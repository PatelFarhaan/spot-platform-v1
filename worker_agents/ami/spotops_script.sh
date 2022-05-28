#! /bin/bash

set -e -x

application_path="/var/opt/spotops/agents"

echo "Providing ubuntu permission to agents folder"
sudo chown ubuntu:ubuntu -R ${application_path}

echo "Running apt update and upgrade"
export DEBIAN_FRONTEND=noninteractive
sudo apt update &&
sudo apt upgrade -y &&

echo "Upgrading the distro"
sudo apt -f install
sudo apt update && sudo apt dist-upgrade -y

echo "Installing AWS CLI"
sudo apt install awscli -y

echo "Installing Python3 and boto3"
sudo apt install python3-pip -y
sudo pip3 install boto3

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

echo "Installing S3-Fuse"
sudo apt install automake autotools-dev fuse g++ git libcurl4-gnutls-dev libfuse-dev libssl-dev libxml2-dev make pkg-config -y
git clone https://github.com/s3fs-fuse/s3fs-fuse.git &&
cd s3fs-fuse &&
./autogen.sh
./configure --prefix=/usr --with-openssl
make
sudo make install
cd ./../ && sudo rm -rf ./s3fs-fuse

echo "Sourcing cloud-init-script"
sudo chmod +x ./spotops_cloud_init.sh
sudo mv ./spotops_cloud_init.sh /etc/profile.d/
source /etc/profile.d/spotops_cloud_init.sh

echo "Creating Cron for checking Disk Size"
crontab -l > mycron
echo "* * * * * python3 ${application_path}/cron_jobs/disk_size_check.py" >> mycron
crontab mycron
rm mycron
