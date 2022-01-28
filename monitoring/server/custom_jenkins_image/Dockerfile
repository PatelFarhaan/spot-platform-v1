FROM jenkins/jenkins:lts

USER root

RUN apt update && apt upgrade -y

RUN apt install awscli -y

RUN apt install packer -y

RUN apt install python3-pip -y