#! /bin/bash

echo "Running apt update and upgrade"
export DEBIAN_FRONTEND=noninteractive
sudo apt update &&
sudo apt upgrade -y &&

echo "Upgrading the distro"
sudo apt -f install
sudo apt update && sudo apt dist-upgrade

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
sudo systemctl restart docker.service &&
sudo usermod -aG docker ${USER}
sudo su - ${USER}
echo "y" | docker plugin install grafana/loki-docker-driver:latest --alias loki --grant-all-permissions