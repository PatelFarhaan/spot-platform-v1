#! /bin/bash

# add a script also to restart when a file updates :=> shell script

set -e -x

echo "Providing ubuntu permission to agents folder"
sudo chown ubuntu:ubuntu -R /var/opt/spotops/agents

echo "Running apt update and upgrade"
export DEBIAN_FRONTEND=noninteractive
sudo apt update &&
sudo apt upgrade -y &&

echo "Upgrading the distro"
sudo apt -f install
sudo apt update && sudo apt dist-upgrade -y

echo "Installing AWS CLI"
sudo apt install awscli -y

echo "Installing Python3"
sudo apt install python3-pip -y

echo "Installing Docker"
sudo apt install apt-transport-https ca-certificates curl software-properties-common -y &&
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - &&
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable" &&
sudo apt update &&
sudo apt install docker-ce -y &&
sudo systemctl restart docker.service &&
sudo curl -L "https://github.com/docker/compose/releases/download/1.28.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose &&
sudo chmod +x /usr/local/bin/docker-compose &&
sudo systemctl restart docker.socket docker.service &&
sudo usermod -aG docker ${USER}
sudo su - ${USER}
echo "y" | sudo docker plugin install grafana/loki-docker-driver:latest --alias loki --grant-all-permissions

echo "Installing S3-Fuse"
sudo apt install automake autotools-dev fuse g++ git libcurl4-gnutls-dev libfuse-dev libssl-dev libxml2-dev make pkg-config -y
git clone https://github.com/s3fs-fuse/s3fs-fuse.git &&
cd s3fs-fuse &&
./autogen.sh
./configure --prefix=/usr --with-openssl
make
sudo make install
cd ./../ && sudo rm -rf ./s3fs-fuse

echo '''
#!/bin/bash

no_of_cores=`nproc --all`
APP_REPLICAS=$(( ($no_of_cores * 2) + 1 ))
export APP_REPLICAS=$APP_REPLICAS

export HOSTNAME=`curl http://169.254.169.254/latest/meta-data/instance-id`
''' >> ./spotops_cloud_init.sh

sudo chmod +x ./spotops_cloud_init.sh
sudo mv ./spotops_cloud_init.sh /etc/profile.d/
source /etc/profile.d/spotops_cloud_init.sh