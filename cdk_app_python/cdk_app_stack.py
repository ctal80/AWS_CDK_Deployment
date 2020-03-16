import random
from aws_cdk import (
    aws_ec2 as ec2,
    core
)
import boto3

class CdkAppStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, props: dict, **kwargs):
       super().__init__(scope, id, **kwargs)
        
      
       print(kwargs)
       print(props)
       ec2b = boto3.client('ec2', region_name=kwargs['env']['region'])
        
       vpc = ec2.Vpc.from_lookup(self, f'{id}-vpc', vpc_name=props['vpc'])
    
       if vpc is None :
           print("VPC lookup error!!!!!!!!!!!!!!!!!!!!!!")
       subnets = []
        
       subnets_response = ec2b.describe_subnets(
            Filters=[
                {
                    'Name': 'tag:Tier',
                    'Values': ['public']
                },
                {
                    'Name': 'vpc-id',
                    'Values': [vpc.vpc_id]
                }
            ]
        )
        
       for s in subnets_response['Subnets']:
            subnets.append(s['SubnetId'])
       self.subnet_id = subnets[random.randint(0, len(subnets)-1)]
        
       sg = ec2.SecurityGroup(self, f'{id}-sg', vpc=vpc)
       sg.add_ingress_rule(
            ec2.Peer.ipv4(props['cidr']),
            ec2.Port.tcp(props['port'])
        )
        
       inst = ec2.CfnInstance(self, f'{id}-inst',
            image_id=props['ami'],
            instance_type=props['inst_type'],
            security_group_ids=[sg.security_group_id],
            subnet_id=self.subnet_id
        )