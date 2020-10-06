from aws_cdk import (
  core
)

from network_topology import NetworkTopology
from webservers import WebServers
from apiservers import APIServers
from database import Database
from load_balancer import LoadBalancer
from security_groups import SecurityGroups

class ThreeTierWebStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, config: dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        topology = NetworkTopology(
          self, 'VPC'
        )

        security_groups = SecurityGroups(
          self, 'SecurityGroups',
          topology.vpc
        )

        webservers = WebServers(
          self, 'WebServers',
          vpc=topology.vpc,
          security_group=security_groups.webserver_security_group,
          instance_type=config["webservers_instance_type"],
        )

        apiservers = APIServers(
          self, 'APIServers',
          vpc=topology.vpc,
          security_group=security_groups.apiserver_security_group,
          instance_type=config["apiservers_instance_type"]
        )

        load_balancer = LoadBalancer(
          self, 'LoadBalancer',
          vpc=topology.vpc,
          security_group=security_groups.alb_security_group,
          instances=webservers.instances
        )

        database = Database(
          self, 'Database',
          vpc=topology.vpc,
          security_group=security_groups.database_security_group,
          master_username=config["rds_master_username"],
          master_password=config["rds_master_password"],
          database_name=config["rds_db_name"]
        )

        