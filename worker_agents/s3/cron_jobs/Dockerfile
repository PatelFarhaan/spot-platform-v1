FROM alpine

COPY . .

RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python

RUN python3 -m ensurepip

RUN pip3 install -r requirements.txt

RUN crontab ./storage_check/disk_storage_check

CMD ["/usr/sbin/crond", "-f"]
