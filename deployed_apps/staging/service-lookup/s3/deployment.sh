#!/bin/bash

export CLIENT_APP_PORT=5000
export AWS_ECR_ID="***REMOVED***.dkr.ecr.us-east-1.amazonaws.com"
export CLIENT_APP_IMAGE="${AWS_ECR_ID}/redflag-service-lookup:9413bc4220760f94a854e028866b50fe769cc2e9"
