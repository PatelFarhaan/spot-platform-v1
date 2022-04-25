FROM jenkins/jenkins:lts

USER root

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update && apt upgrade -y

RUN apt install wget

RUN wget -qO /usr/local/bin/yq https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64 && chmod a+x /usr/local/bin/yq

RUN apt install apt-utils -y

RUN apt install python3-pip -y

RUN pip3 install python-dateutil

RUN apt install virtualenv -y

RUN apt install awscli -y

RUN apt install jq -y

RUN pip3 install boto3

RUN pip3 install requests

RUN pip3 install python-dateutil

RUN apt update && apt install -y lsb-release && apt-get clean all

RUN apt install software-properties-common -y

RUN curl -fsSL https://apt.releases.hashicorp.com/gpg | apt-key add -

RUN apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"

RUN apt-get update && apt-get install packer

RUN git config --global user.email "redflagAutomationUser@***REMOVED***"

RUN git config --global user.name "redflagAutomationUser"

RUN mkdir /root/.aws

COPY credentials /root/.aws/credentials

RUN apt install -y gnupg software-properties-common curl

RUN curl -fsSL https://apt.releases.hashicorp.com/gpg | apt-key add -

RUN apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"

RUN apt update && apt install terraform
