#! /bin/bash

export DEBIAN_FRONTEND=noninteractive
sudo apt update &&
sudo apt upgrade -y &&
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

sudo apt install ec2-instance-connect -y
rm -rf local-exec-script.sh ami.pkr.hcl
cd docker_agents &&
sudo docker-compose up -d --build
sudo snap install amazon-ssm-agent --classic && sudo snap start amazon-ssm-agent

#https://devopscube.com/docker-containers-as-build-slaves-jenkins/


ls /usr/share/zoneinfo
echo "America/New_York" | sudo tee /etc/timezone && sudo dpkg-reconfigure --frontend noninteractive tzdata

sudo ln -sf /usr/share/zoneinfo/America/Los_Angeles /etc/localtime