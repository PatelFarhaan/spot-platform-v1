# create a multi-stage build and hardern the image
FROM python:3.9.9-slim

EXPOSE 5000
WORKDIR /application

RUN apt update && apt upgrade -y
RUN apt install cron vim -y
RUN python3 -m pip install --upgrade pip

COPY app.py /application
COPY aws_services.py /application
COPY aws_services.py /application
COPY slack_notify.py /application
COPY requirements.txt /application
COPY file_functions.py /application
COPY common_functions.py /application
COPY create_cron_task.sh /application

RUN pip3 install -r requirements.txt
#RUN bash create_cron_task.sh

CMD ["python3", "app.py"]