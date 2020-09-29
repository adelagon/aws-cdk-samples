from aws_cdk import (
  aws_ec2 as ec2,
  core
)

class NetworkTopology(core.Construct):

  @property
  def vpc(self):
    return self._vpc

  @property
  def public_subnets(self):
    return self._public_subnets

  @property
  def private_subnets(self):
    return self._private_subnets

  def __init__(self, scope: core.Construct, id: str, **kwargs):
    super().__init__(scope, id, **kwargs)

    self._private_subnets = ec2.SubnetConfiguration(name="private", subnet_type=ec2.SubnetType.PRIVATE)
    self._public_subnets = ec2.SubnetConfiguration(name="public", subnet_type=ec2.SubnetType.PUBLIC)

    self._vpc = ec2.Vpc(
      self, id,
      subnet_configuration=[
        self._private_subnets,
        self._public_subnets
      ],
      nat_gateways=1
    )

