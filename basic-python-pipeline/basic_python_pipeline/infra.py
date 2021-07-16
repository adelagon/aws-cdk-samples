from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    core
)

class Infra(core.Construct):

    @property
    def vpc(self):
        return self._vpc
    
    @property
    def cluster(self):
        return self._cluster

    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # VPC
        self._vpc = ec2.Vpc(
            self, "PythonVPC",
            max_azs=2
        )
        
        # Cluster
        self._cluster = ecs.Cluster(
            self, "PythonCluster",
            vpc=self._vpc
        )

        