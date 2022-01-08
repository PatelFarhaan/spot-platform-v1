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
- Deployment Rollback as needed
- Managed Multi-region deployment
- Managed Ops and scaling for end users
- Email Services inbuild on application on-boarding
- Monitoring and altering for all apps on the platform
- Managed Database services (MySQL, Psql, and Mongo)
- Cost Optimization as major services are hosted on SPOT
- Webhooks for custom integrations for almost all services
- List of all resource usage integrated right in the dashboard
- Dashboard to view all instances, services, and service accounts
- HA system and implemented Fail-over for almost all major services
- Automated webhook for increasing the volume size after it reaches a threshold


# OWNER AND MAINTAINER
**[FARHAAN PATEL](https://github.com/PatelFarhaan "FARHAAN PATEL")**


# TODO:
- [ ] EBS Affinity per AZ
- [ ] Increase and decrease volume size
- [ ] Certifacte expire and renew alters
- [ ] Support multiple instances for SPOT
- [ ] Create and manage the ACM accordingly
- [ ] Run terrafrom on EC2 through ASSUME ROLE
- [ ] Open LB for all availability zones and public subnets
- [ ] Download/Upload an SSH key for enduser if he does not have one
- [ ] Create a docker-compose file for all agents -> End user instances
- [ ] To know when to use and replace t3 unlimited to standard and vice versa
- [ ] Create a docker-compile file for automation of Jenkins and other stuff -> server side
- [ ] Dynamically change the gunicorn processes and threads as per instance cores in each deployment
- [ ] Build an end user dashboard where they can import their keys and check their instance utilization
- [ ] Support EFS attachment for data persistance and ingest code to attach the EFS to instance at launch time
- [ ] Replace unhealthy instances
- [ ] Create Events Rules for autoscaling and spot in Cloudwatch
- [ ] Create an activity page for the frontend where all events from cloudwatch will be displayed
- [ ] Dashboard where it displays all ASG and all instances in each, buttons on instances to connect to it + health in green or red
- [ ] Checks on ebs volume threshold reaches beyond a certain limit
- [ ] Validate Subscription is from SNS -> Decode the Signature and compare it with the token
- [ ] Add Resource limits to docker container in compose file


# END USER DASHBOARD
- [ ] SemaPhore Docs for Ansible Agents
- [ ] Logstash and Kibana for APM -> End user dashboard
- [ ] Integrate Nexus as a docker registry -> End user dashboard

# CURRENTLY, WORKING ON
How to store promwtheus data on disk
prometheus alerts
Add authentication for /metrics endpoint

agent to update the prometheus file dynamically and deplot all this via terraform

Migrate to Spot Fleet
Install monitoring agents to analyze the memory
Jenkins CI to create custom baked images using Packer


# CUSTOM COMMANDS
```bash
aws ec2 describe-subnets --filter Name=vpc-id,Values=vpc-8d6cc4f6 --query 'Subnets[?MapPublicIpOnLaunch==`false`].SubnetId'
```

# LINKS
1. Run Jenkins CI on SPOT Fleet: https://www.youtube.com/watch?v=8gGItacZjps
2. traefik: https://doc.traefik.io/traefik/routing/services/ and https://www.indivar.com/blog/how-to-setup-traefik-portainer-on-ubuntu1804/ and https://hub.docker.com/_/traefik
3. Loki https://grafana.com/grafana/dashboards/14055 and https://grafana.com/grafana/dashboards/12611
4. Concul: https://www.consul.io/docs/connect/observability/ui-visualization
5. Cloudwatch spot sns: https://ec2spotworkshops.com/running_spark_apps_with_emr_on_spot_instances/tracking_spot_interruptions.html
6. All Grafana Dashboards: https://play.grafana.org/d/000000012/grafana-play-home?orgId=1
7. https://pinpoint-apm.github.io/pinpoint/#


# KEYPOINTS
1. ASG and LB will only have public subnets else public ip will not be provided


Grafana dashboards used:
