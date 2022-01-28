# <==================================================================================================>
#                                          IMPORTS
# <==================================================================================================>
import os
import jenkins


# <==================================================================================================>
#                                         DELETE A NEW JENKINS JOB
# <==================================================================================================>
def delete_job(job_name):
    try:
        server.delete_job(job_name)
    except Exception as e:
        print(f"There was an error creating the jenkins job: {e}")


# <==================================================================================================>
#                                          MAIN FUNCTION
# <==================================================================================================>
if __name__ == '__main__':
    new_job_name = "test"
    jenkins_base_url = os.getenv("JENKINS_BASE_URL")
    jenkins_username = os.getenv("JENKINS_USERNAME")
    jenkins_password = os.getenv("JENKINS_PASSWORD")

    server = jenkins.Jenkins(jenkins_base_url,
                             username=jenkins_username,
                             password=jenkins_password)

    delete_job(new_job_name)
