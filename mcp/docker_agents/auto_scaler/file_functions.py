# <==================================================================================================>
#                                         IMPORTS
# <==================================================================================================>
import os
import json
from datetime import datetime, timedelta


# <==================================================================================================>
#                                    CREATE A FILE IF DOES NOT EXIST
# <==================================================================================================>
def create_a_file_if_does_not_exists(filename: str):
    if not os.path.exists(filename):
        save_json_file(filename, {})


# <==================================================================================================>
#                                         READ A JSON FILE
# <==================================================================================================>
def read_json_file(filename: str):
    return json.load(open(filename))


# <==================================================================================================>
#                                         WRITE JSON TO A FILE
# <==================================================================================================>
def save_json_file(filename: str, file_content: json):
    with open(filename, 'w') as outfile:
        json.dump(file_content, outfile, indent=4)


# <==================================================================================================>
#                                      UPDATE COOLDOWN PERIOD
# <==================================================================================================>
def updated_cooldown_period(filename):
    cool_down_period_mins = 5
    content = read_json_file(filename)
    content["cool_down_period_ts"] = str(datetime.utcnow() + timedelta(minutes=cool_down_period_mins))
    save_json_file(filename, content)
