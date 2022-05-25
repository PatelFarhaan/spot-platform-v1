#!/bin/bash

export CLIENT_APP_PORT=5000
export AWS_ECR_ID="***REMOVED***.dkr.ecr.us-east-1.amazonaws.com"
export CLIENT_APP_IMAGE="${AWS_ECR_ID}/redflag-media-lookup:prod-1"