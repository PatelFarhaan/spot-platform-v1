# <==================================================================================================>
#                                          IMPORTS
# <==================================================================================================>
import shutil
import sys
from datetime import datetime
from os import environ

from .aws import AWS


# <==================================================================================================>
#                                       DISK SPACE CHECK UTILITY
# <==================================================================================================>
class DiskSpaceChecker(AWS):
    def __init__(self):
        super().__init__()
        self.log_obj = dict()
        self.autoscale = "autoscaling"
        self.log_obj["instance_id"] = self.instance_id
        self.free_disk_threshold_gb = int(environ["free_disk_threshold_in_gb"])
        self.log_obj["current_dt"] = datetime.now().strftime("%b %d %Y, %H:%M:%S")

    def is_disk_full(self):
        total, used, free = shutil.disk_usage("/")
        _free = free // (2 ** 30)

        if _free <= self.free_disk_threshold_gb:
            self.log_obj["disk_full"] = True
            self.log_obj["remaining"] = f"{_free} GB"
            return True

        self.log_obj["disk_full"] = False
        self.log_obj["remaining"] = f"{_free} GB"
        print(self.log_obj)
        sys.exit(0)

    def mark_instance_as_unhealthy(self):
        asg_client = self.get_boto3_client(self.autoscale)

        response = asg_client.set_instance_health(
            HealthStatus="Unhealthy",
            InstanceId=self.instance_id
        )
        self.log_obj["unhealthy_api_response"] = response

    def run(self):
        self.is_disk_full()
        self.mark_instance_as_unhealthy()
        print(self.log_obj)


# <==================================================================================================>
#                                          MAIN CALLING FUNCTION
# <==================================================================================================>
if __name__ == '__main__':
    disk_utility_obj = DiskSpaceChecker()
    disk_utility_obj.run()
