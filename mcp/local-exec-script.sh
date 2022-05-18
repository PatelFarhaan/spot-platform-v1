#!/bin/bash

volume_size=10
company_name="redflag"
instance_size='r5a.xlarge'
key_name_pair='redflag_ec2'
subnet_id='subnet-2ea78701'
iam_profile="r-aws-manager-role"
security_group='sg-016d6adc3830261ae'
volume_tags="Tags=[{Key=Name,Value=mcp-$company_name}]"
instance_tags="Tags=[{Key=Name,Value=mcp-$company_name}]"
ami_id=$(cat manifest.json| jq -r '.builds[0].artifact_id' | cut -d ':' -f 2)

echo "Creating instance from AMI: $ami_id"
aws ec2 run-instances \
        --image-id=$ami_id \
        --subnet-id=$subnet_id \
        --key-name=$key_name_pair \
        --instance-type=$instance_size \
        --security-group-ids=$security_group \
        --iam-instance-profile="Name=$iam_profile" \
        --tag-specifications ResourceType=volume,${volume_tags} ResourceType=instance,${instance_tags} \
        --block-device-mappings="DeviceName=/dev/sda1,Ebs={VolumeSize=$volume_size}" | jq -r '.Instances[0].InstanceId'
