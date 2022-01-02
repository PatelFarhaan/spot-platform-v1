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
- [ ] Run terrafrom on EC2 through ASSUME ROLE
- [ ] Download/Upload an SSH key for enduser if he does not have one
- [ ] Open LB for all availability zones and public subnets
- [ ] Dynamically change the gunicorn processes and threads as per instance cores in each deployment
- [ ] Create and manage the ACM accordingly
- [ ] Certifacte expire and renew alters
- [ ] Increase and decrease volume size
- [ ] Build an end user dashboard where they can import their keys and check their instance utilization
- [ ] EBS Affinity per AZ
- [ ] Support EFS attachment for data persistance and ingest code to attach the EFS to instance at launch time
- [ ] Create a docker-compose file for all agents -> End user instances
- [ ] Create a docker-compile file for automation of Jenkins and other stuff -> server side
- [ ] To know when to use and replace t3 unlimited to standard and vice versa
- [ ] Support multiple instances for SPOT


# CURRENTLY WORKING ON
Migrate to Spot Fleet
Jenkins CI to create custom baked images using Packer


# CUSTOM COMMANDS
```bash
aws ec2 describe-subnets --filter Name=vpc-id,Values=vpc-8d6cc4f6 --query 'Subnets[?MapPublicIpOnLaunch==`false`].SubnetId'
```
