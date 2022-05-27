import shutil


def is_disk_full():
    total, used, free = shutil.disk_usage("/")
    _free = free // (2 ** 30)

    if _free <= free_disk_threshold:
        return True
    return False


if __name__ == '__main__':
    free_disk_threshold = 1
    available_disk_size = is_disk_full()

"""
export HOSTNAME=`curl http://169.254.169.254/latest/meta-data/instance-id`

aws autoscaling set-instance-health --instance-id i-02c0c737ffdaade71 --health-status Unhealthy
"""