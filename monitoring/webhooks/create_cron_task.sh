#write out current crontab
crontab -l > mycron

#echo new cron into cron file
echo "*/30 * * * * cd /application && python3 update_prometheus_file.py" >> mycron
#install new cron file
crontab mycron
rm mycron