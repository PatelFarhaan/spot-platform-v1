FROM jenkins/jenkins:lts

USER root

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update && apt upgrade -y

RUN apt install wget apt-utils python3-pip virtualenv lsb-release awscli jq software-properties-common gnupg software-properties-common curl -y

RUN pip3 install python-dateutil boto3 requests

RUN wget -qO /usr/local/bin/yq https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64 && chmod a+x /usr/local/bin/yq

RUN curl -fsSL https://apt.releases.hashicorp.com/gpg | apt-key add -

RUN apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"

RUN git config --global user.email "redflagAutomationUser@***REMOVED***"

RUN git config --global user.name "redflagAutomationUser"

RUN curl -fsSL https://apt.releases.hashicorp.com/gpg | apt-key add -

RUN apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"

RUN apt update && apt-get clean all && apt install packer terraform