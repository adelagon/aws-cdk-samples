from aws_cdk import (
  aws_ec2 as ec2,
  core
)

class SecurityGroups(core.Construct):

  @property
  def alb_security_group(self):
    return self._alb_security_group

  @property
  def webserver_security_group(self):
    return self._webserver_security_group

  @property
  def apiserver_security_group(self):
    return self._apiserver_security_group

  @property
  def database_security_group(self):
    return self._database_security_group

  def __init__(self, scope: core.Construct, id: str, vpc: ec2.IVpc, **kwargs):
    super().__init__(scope, id, **kwargs)

    # Load Balancer Security Group
    self._alb_security_group = ec2.SecurityGroup(
      self, "LBSG",
      vpc=vpc
    )
    self._alb_security_group.add_ingress_rule(
      ec2.Peer.any_ipv4(),
      ec2.Port.tcp(80),
    )

    # Web Server Security Group
    self._webserver_security_group = ec2.SecurityGroup(
      self, "WebServerSG",
      vpc=vpc
    )
    self._webserver_security_group.add_ingress_rule(
      self._alb_security_group,
      ec2.Port.tcp(80),
    )
    
    # API Server Security Group
    self._apiserver_security_group = ec2.SecurityGroup(
      self, "APIServerSG",
      vpc=vpc
    )
    self._apiserver_security_group.add_ingress_rule(
      self._webserver_security_group,
      ec2.Port.tcp(8080),
    )

    # Database Security Group
    self._database_security_group = ec2.SecurityGroup(
      self, "DBSG",
      vpc=vpc
    )
    self._database_security_group.add_ingress_rule(
      self._apiserver_security_group,
      ec2.Port.tcp(3306)
    )