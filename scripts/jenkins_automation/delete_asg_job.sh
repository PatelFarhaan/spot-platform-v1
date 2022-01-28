#! /bin/bash


current_path=`pwd`
cd ../.. &&
source venv/bin/activate
cd "$current_path" &&
python3 delete_asg_job.py
