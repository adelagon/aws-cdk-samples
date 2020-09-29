from aws_cdk import (
  aws_rds as rds,
  aws_ec2 as ec2,
  core
)

class Database(core.Construct):
  @property
  def database(self):
    return self._database

  def __init__(self, app: core.App, id: str, master_username: str, master_password: str, database_name: str, vpc: ec2.IVpc, **kwargs):
    super().__init__(app, id, **kwargs)

    # RDS - MySQL. It defaults to VPC's Private Subnets unless specified
    self._database = rds.DatabaseInstance(
      self, id,
      master_username=master_username,
      master_user_password=core.SecretValue.plain_text(master_password),
      database_name=database_name,
      engine=rds.DatabaseInstanceEngine.mysql(
        version=rds.MysqlEngineVersion.VER_8_0_16,
      ),
      vpc=vpc,
      port=3306,
      instance_type=ec2.InstanceType.of(
        ec2.InstanceClass.BURSTABLE3,
        ec2.InstanceSize.MICRO
      ),
      removal_policy=core.RemovalPolicy.DESTROY,
      deletion_protection=False
    )