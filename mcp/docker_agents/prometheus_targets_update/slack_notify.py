# <==================================================================================================>
#                                          IMPORTS
# <==================================================================================================>
import sys
import json
import requests


# <==================================================================================================>
#                                          SEND SLACK NOTIFICATION
# <==================================================================================================>
def send_slack_notification(data={}, failed=False):
    url = "***REMOVED***"

    print(data, failed)
    if failed:
        title = "*PROMETHEUS UPDATE FAILED*"
        links = "*LokiURL*: http://env-a-manager.***REMOVED***/d/liz0yRCZz/platform-logging?orgId=1&var-application=mcp&var-environment=staging&var-container=prometheus_target_update&var-search="
    else:
        topic_arn = data.get("TopicArn")
        subscribe_url = data.get("SubscribeURL")
        title = "*NEW SUBSCRIPTION*"
        links = f"*TopicArn:* {topic_arn} \n*SubscribeURL:* {subscribe_url}"

    slack_data = {
        "username": "SpotOpsBot",
        "icon_emoji": ":busstop:",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{title}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{links}"
                }
            }
        ]
    }
    byte_length = str(sys.getsizeof(slack_data))
    headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
    try:
        response = requests.post(url, data=json.dumps(slack_data), headers=headers)
        if response.status_code == 200:
            print("Success sending slack message!!!")
        else:
            print(f"Failed: {response.status_code}")
    except Exception as e:
        print("Failed sending slack message!!!", e)
