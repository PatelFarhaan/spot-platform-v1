# create a multi-stage build and hardern the image
FROM python:3.9.9-slim

RUN apt update && apt upgrade -y

RUN apt install cron vim -y

EXPOSE 5000

WORKDIR /application

RUN python3 -m pip install --upgrade pip

ENV AWS_REGION=us-east-1

ENV AUTO_SCALING_GROUP=lookup-service-spot-as

COPY app.py /application

COPY create_cron_task.sh /application

COPY update_prometheus_file_cron.py /application

COPY requirements.txt /application

RUN pip3 install -r requirements.txt

RUN bash create_cron_task.sh

CMD ["python3", "app.py"]