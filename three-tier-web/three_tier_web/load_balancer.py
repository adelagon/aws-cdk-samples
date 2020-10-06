from aws_cdk import (
  aws_ec2 as ec2,
  aws_elasticloadbalancingv2 as elbv2,
  core
)

class LoadBalancer(core.Construct):

  @property
  def alb(self):
    return self._alb
    
  def __init__(self, scope: core.Construct, id: str, vpc: ec2.IVpc, security_group: ec2.ISecurityGroup, instances: list, **kwargs):
    super().__init__(scope, id, **kwargs)

    self._tg = elbv2.ApplicationTargetGroup(
      self, "TG",
      port=80,
      vpc=vpc,
    )

    for instance in instances:
      self._tg.add_target(
        elbv2.InstanceTarget(
          instance.instance_id,
          port=80
        )
      )

    self._alb = elbv2.ApplicationLoadBalancer(
      self, "LB",
      vpc=vpc,
      internet_facing=True,
      security_group=security_group
    )

    listener = self._alb.add_listener("Listener", port=80, default_target_groups=[self._tg])