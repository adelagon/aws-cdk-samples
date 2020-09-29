from aws_cdk import (
  aws_ec2 as ec2,
  core
)

class WebServers(core.Construct):

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

    # Security Group
    security_group = ec2.SecurityGroup(
      self, "WebServerSG",
      vpc=vpc
    )
    security_group.add_ingress_rule(
      ec2.Peer.any_ipv4(),
      ec2.Port.tcp(80),
    )

    # Fetch the bootstrap script
    data = open("./three_tier_web/userdata.sh", "rb").read()
    user_data = ec2.UserData.for_linux()
    user_data.add_commands(str(data, 'utf-8'))

    # Launch Web Server Instance Per Public Subnet
    self._instances = []
    i = 0
    for subnet in vpc.select_subnets(subnet_type=ec2.SubnetType.PUBLIC).subnets:
      subnet_selection = ec2.SubnetSelection(subnets=[subnet])
      self._instances.append(
        ec2.Instance(
        self, id+str(i),
        instance_type=ec2.InstanceType(instance_type),
        vpc=vpc,
        vpc_subnets=subnet_selection,
        machine_image=amzn_linux,
        user_data=user_data,
        security_group=security_group
        )
      )
      i += 1