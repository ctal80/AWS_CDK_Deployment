from aws_cdk import (
     aws_elasticache as elasticache,
     aws_ec2 as ec2,
     core
)


class RedisCluster(core.Stack):
     def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Create new VPC
        vpc = ec2.Vpc(
            self, "Default",
            max_azs=3,
            nat_gateways=1,
            cidr=ec2.Vpc.DEFAULT_CIDR_RANGE,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Private-Subnet",
                    subnet_type=ec2.SubnetType.PRIVATE,
                    cidr_mask=19,
                    reserved=None
                ),
                ec2.SubnetConfiguration(
                    name="Public-Subnet",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=22,
                    reserved=None
                ),
                ec2.SubnetConfiguration(
                    name="Isolated-Subnet",
                    subnet_type=ec2.SubnetType.ISOLATED,
                    cidr_mask=28,
                    reserved=None
                )
            ]
        )
        
         # Try subnet group
        subnet_group = elasticache.CfnSubnetGroup(
            scope=self,
            id="Testing-Subnet-Group",
            description="Group private subnets for redis access.",
            subnet_ids=[subnet.subnet_id for subnet in vpc.private_subnets],
            cache_subnet_group_name="test-int-private-subnets"
        )
        redis_security_group = ec2.SecurityGroup(
            scope=self,
            id="TEMP-redis-SG",
            vpc=vpc,
            allow_all_outbound=False
        )

        redis_cluster = elasticache.CfnCacheCluster(
            scope=self,
            cache_node_type="cache.t2.micro",
            id="testmy-redis",
            engine="redis",
            num_cache_nodes=1,
            vpc_security_group_ids=[redis_security_group.security_group_id],
            cache_subnet_group_name=subnet_group.ref,
            cluster_name="testmy-redis"
        )
    
    
