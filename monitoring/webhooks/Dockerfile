# create a multi-stage build and hardern the image
FROM python:3.9.9-slim

EXPOSE 5000

WORKDIR /application

RUN python3 -m pip install --upgrade pip

ENV AWS_REGION=us-east-1

ENV AUTO_SCALING_GROUP=lookup-service-spot-as

COPY update_prometheus_file.py /application

COPY requirements.txt /application

RUN pip3 install -r requirements.txt

CMD ["python3", "update_prometheus_file.py"]