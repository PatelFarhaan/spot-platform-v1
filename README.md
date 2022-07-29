# SPOT PLATFORM

This is a managed platform as a service (PaaS), to manage and scale new/existing workloads on SPOT instances. The 
architecture uses a minimal On-Demand/Reserved instances as per need to maintain high availability of the application. 
Application is scaled on SPOT as per need and On-Demand/Reserved instances are added if SPOT is unavailable to meet the 
need of the traffic.


# TOOLS AND FEATURES
- [ ] Terraform
- [ ] Custom Autoscaler
- [ ] Jenkins for CI and CD
- [ ] CodeDeploy/Ansible for CD
- [ ] Scripting (Python and Bash)
- [ ] Ansible for application environment vars update
- [ ] Uptime Kuma for service monitoring: Need to evsluate
- [ ] Monitoring Stack (Promtail, Prometheus, Grafana and Loki)
- [ ] Docker to install and configure agents in the form of Backed AMI

https://www.youtube.com/watch?v=Fwsyq5zIhsg

# Services 
- Single click deployment
- Cost and Savings Dashboard
- Managed Multi-region deployment
- Managed Ops and scaling for end users
- Monitoring and altering for all apps on the platform
- Cost Optimization as major services are hosted on SPOT
- Webhooks for custom integrations for almost all services
- List of all resource usage integrated right in the dashboard
- Automated webhook for increasing the volume size after it reaches a threshold
- Deployment Rollback as needed -> Possible using docker as it's independent on the infra
- Dashboard to view all instances, services, and service accounts and a drop-view from end url (R53) to services


# OWNER AND MAINTAINER
**[FARHAAN PATEL](https://github.com/PatelFarhaan "FARHAAN PATEL")**


Commands:
aws sns confirm-subscription -> Automate the process: send out slack message
aws ec2 describe-instance-type-offerings --location-type availability-zone  --filters Name=instance-type,Values=r5b.2xlarge --region us-east-1 --output table
ec2-instance-selector --vcpus 8 --memory=32  --usage-class spot  --cpu-architecture x86_64 --region us-east-1 -o table
