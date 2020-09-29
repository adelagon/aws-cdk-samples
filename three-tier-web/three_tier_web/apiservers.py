from aws_cdk import (
  aws_ec2 as ec2,
  core
)

class APIServers(core.Construct):

  @property
  def instances(self):
    return self._instances

  def __init__(self, scope: core.Construct, id: str, instance_type: str, vpc: ec2.IVpc, **kwargs):
    super().__init__(scope, id, **kwargs)

    # AMI
    amzn_linux = ec2.MachineImage.latest_amazon_linux(
      generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
      edition=ec2.AmazonLinuxEdition.STANDARD,
      virtualization=ec2.AmazonLinuxVirt.HVM,
      storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE,
      cpu_type=ec2.AmazonLinuxCpuType.X86_64
    )

    # Launch API Server Instance Per Private Subnet
    self._instances = []
    i = 0
    for subnet in vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE).subnets:
      self._instances.append(
        ec2.Instance(
        self, id+str(i),
        instance_type=ec2.InstanceType(instance_type),
        vpc=vpc,
        vpc_subnets=subnet,
        machine_image=amzn_linux
        )
      )
      i += 1