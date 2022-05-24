# create a multi-stage build and hardern the image
FROM python:3.9.9-slim

EXPOSE 5000
WORKDIR /application

RUN apt update && apt upgrade -y
RUN apt install awscli -y
RUN apt install cron vim -y
RUN python3 -m pip install --upgrade pip

COPY requirements.txt /application
RUN pip3 install -r requirements.txt

COPY app.py /application
COPY aws_services.py /application
COPY aws_services.py /application
COPY slack_notify.py /application
COPY file_functions.py /application
COPY common_functions.py /application
COPY cron_file_update.py /application

COPY target_update_cron /etc/cron.d/target_update_cron
RUN chmod 0644 /etc/cron.d/target_update_cron
RUN crontab  /etc/cron.d/target_update_cron
RUN touch /var/log/cron.log
RUN cron

RUN #crontab -l | { cat; echo "*/30 * * * * python3 /application/cron_file_update.py"; } | crontab -
CMD ["python3", "app.py"]