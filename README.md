# SPOT PLATFORM

This is a managed platform as a service (PaaS), to manage and scale new/existing workloads on SPOT instances. The 
architecture uses a minimal On-Demand/Reserved instances as per need to maintain high availability of the application. 
Application is scaled on SPOT as per need and On-Demand/Reserved instances are added if SPOT is unavailable to meet the 
need of the traffic.


# TOOLS AND FEATURES
- [ ] Terraform
- [ ] Jenkins for CI
- [ ] Custom Autoscaler
- [ ] CodeDeploy for CD
- [ ] Database Management
- [ ] Scripting (Python and Bash)
- [ ] Packer for custom backed images
- [ ] Uptime Kuma for service monitoring
- [ ] Docker to install and configure agents
- [ ] Ansible for platform update and upgrade
- [ ] Monitoring Stack (Promtail, Grafana, Loki and Kibana)


# Services 
- Single click deployment
- Cost and Savings Dashboard
- Managed Multi-region deployment
- Managed Ops and scaling for end users
- Service to decrease the volume size as needed
- Email Services in build on application on-boarding
- Monitoring and altering for all apps on the platform
- Managed Database services (MySQL, Psql, and Mongo)
- Cost Optimization as major services are hosted on SPOT
- Webhooks for custom integrations for almost all services
- List of all resource usage integrated right in the dashboard
- HA system and implemented Fail-over for almost all major services
- Automated webhook for increasing the volume size after it reaches a threshold
- Deployment Rollback as needed -> Possible using docker as it's independent on the infra
- Dashboard to view all instances, services, and service accounts and a drop-view from end url (R53) to services


# OWNER AND MAINTAINER
**[FARHAAN PATEL](https://github.com/PatelFarhaan "FARHAAN PATEL")**


# TODO:
- [ ] EBS Affinity per AZ
- [ ] Replace unhealthy instances
- [ ] Increase and decrease volume size
- [ ] Certificate expire and renew alters
- [ ] Support multiple instances for SPOT
- [ ] Create and manage the ACM accordingly
- [ ] Locust.io for load testing on medium.com
- [ ] Run terraform on EC2 through ASSUME ROLE
- [ ] Regular S3 backup of the monitoring node data
- [ ] Open LB for all availability zones and public subnets
- [ ] ASG not autoscaling while launch template is modified
- [ ] Define max servers and don't exceed the max at any cost
- [ ] Dynamic node provisioning in Jenkins for running builds
- [ ] Add Resource limits to docker container in compose file
- [ ] Create Events Rules for autoscaling and spot in Cloudwatch
- [ ] Checks on ebs volume threshold reaches beyond a certain limit
- [ ] Download/Upload an SSH key for end user if he does not have one
- [ ] Create a docker-compose file for all agents -> End user instances
- [ ] To know when to use and replace t3 unlimited to standard and vice versa
- [ ] Create a docker-compile file for automation of Jenkins and other stuff -> server side
- [ ] Validate Subscription is from SNS -> Decode the Signature and compare it with the token
- [ ] Create an activity page for the frontend where all events from cloudwatch will be displayed
- [ ] Dynamically change the gunicorn processes and threads as per instance cores in each deployment
- [ ] Build an end user dashboard where they can import their keys and check their instance utilization
- [ ] Able to spin a new environment based on any existing one along with db and everything for testing
- [ ] If the env is not active for x min's, disable the env to save cost -> Non prod env/ option from UI
- [ ] Support EFS attachment for data persistence and ingest code to attach the EFS to instance at launch time
- [ ] Dashboard where it displays all ASG and all instances in each, buttons on instances to connect to it + health in green or red


# END USER DASHBOARD
- [ ] SemaPhore Docs for Ansible Agents
- [ ] Logstash and Kibana for APM -> End user dashboard
- [ ] Integrate Nexus as a docker registry -> End user dashboard

# CURRENTLY, WORKING ON
How to store prometheus data on disk
prometheus alerts
Add authentication for /metrics endpoint

agent to update the prometheus file dynamically and deploy all this via terraform

Jenkins CI to create custom baked images using Packer


# CUSTOM COMMANDS
```bash
aws ec2 describe-subnets --filter Name=vpc-id,Values=vpc-8d6cc4f6 --query 'Subnets[?MapPublicIpOnLaunch==`false`].SubnetId'
```

# LINKS
1. Run Jenkins CI on SPOT Fleet: https://www.youtube.com/watch?v=8gGItacZjps
2. Loki https://grafana.com/grafana/dashboards/14055 and https://grafana.com/grafana/dashboards/12611
3. Concul: https://www.consul.io/docs/connect/observability/ui-visualization
4. Cloudwatch spot sns: https://ec2spotworkshops.com/running_spark_apps_with_emr_on_spot_instances/tracking_spot_interruptions.html
5. All Grafana Dashboards: https://play.grafana.org/d/000000012/grafana-play-home?orgId=1
6. https://pinpoint-apm.github.io/pinpoint/#
7. Grafana dashboard for different databases, mongo: 8339
8. Alerting Rules: https://awesome-prometheus-alerts.grep.to/rules.html
9. Dynamic Jenkins Node provisioning: https://www.cloudbees.com/blog/how-to-install-and-run-jenkins-with-docker-compose
10. Change jenkins logo and text: https://medium.com/@elhayefrat/replace-jenkins-logo-and-text-to-your-choice-in-jenkinsui-f7d35daed25b
11. ELK on docker: https://github.com/deviantony/docker-elk
12. Nginx proxy manager, supervisord GUI


# KEYPOINTS
1. ASG and LB will only have public subnets else public ip will not be provided


Grafana dashboards used:


Commands:
aws sns confirm-subscription -> Automate the process
aws ec2 describe-instance-type-offerings --location-type availability-zone  --filters Name=instance-type,Values=r5b.2xlarge --region us-east-1 --output table
ec2-instance-selector --vcpus 8 --memory=32  --usage-class spot  --cpu-architecture x86_64 --region us-east-1 -o table


get all public subnet in a vpc for autoscaling
if we are considering 2 instances, one is available in 2 az and other in 3. How to handle that condition?
make sure all instances have a public ip address


get all resources in private zone