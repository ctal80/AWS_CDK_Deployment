#!/usr/bin/env python3

import os, sys
from aws_cdk import core
from vpc_cdk.vpc_cdk_stack import VpcCdkStack
from helpers import Inputs
from cdk_app_python.cdk_app_stack import CdkAppStack
from cdk_lambda_dynamodb_fargate.cdk_fargate_stack import FargateStack
from cdk_lambda_dynamodb_fargate.cdk_lambda_dynamodb_stack import CdkLambdaDynamodbStack
from elastic_cache.cdk_redis import RedisCluster

app = core.App()
i = Inputs()


account = '437640264121'
region =  'us-east-1'
#eploy_env = i.get(app, 'DeployEnv')
deploy_env = 'dev'
base_cidr = i.get(app, 'BaseCidr')[region][deploy_env]
aws_dns = i.get(app, 'AwsDns')
high_availability = i.get(app, 'HighAvailability')[deploy_env]


vpc = i.get(app, 'Vpc')['dev']
cidr = i.get(app, 'PublicCidr')
os = i.get(app, 'OperatingSystem')
port = i.get(app, 'ConnectPortByOs')[os]
ami = i.get(app, 'AmiByOs')
inst_type = i.get(app, 'InstanceType')


env={
            'account' : '437640264121',
            'region' : 'eu-west-1'
        }

props={
            'deploy_env' : deploy_env,
            'vpc': vpc,
            'cidr': cidr,
            'port': port,
            'os': os,
            'ami': ami[region][os],
            'inst_type': inst_type
        }
        
        

#CdkAppStack(app, "cdk-app", props = props, env=env)

env2={
        'account': account,
        'region': region,
        }
    
props2={
        'cidr': base_cidr,
        'deploy_env': deploy_env,
        'aws_dns': aws_dns,
        'ha': high_availability,
    }



VpcCdkStack(app, "vpc-cdk",props = props2, env = env2)
CdkLambdaDynamodbStack(app, "cdk-lambda-dynamodb", env=env)
FargateStack(app, "cdk-fargate", env=env)
RedisCluster(app, "RedisCluster", env=env)

app.synth()