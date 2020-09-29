from aws_cdk import (
  core
)
from network_topology import NetworkTopology
from webservers import WebServers
from apiservers import APIServers
from database import Database
from load_balancer import LoadBalancer

class ThreeTierWebStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, config: dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        topology = NetworkTopology(
          self, 'VPC'
        )

        webservers = WebServers(
          self, 'WebServers',
          vpc=topology.vpc,
          instance_type=config["webservers_instance_type"]
        )

        apiservers = APIServers(
          self, 'APIServers',
          vpc=topology.vpc,
          instance_type=config["apiservers_instance_type"]
        )

        database = Database(
          self, 'Database',
          vpc=topology.vpc,
          master_username=config["rds_master_username"],
          master_password=config["rds_master_password"],
          database_name=config["rds_db_name"]
        )

        load_balancer = LoadBalancer(
          self, 'LoadBalancer',
          vpc=topology.vpc,
          instances=webservers.instances
        )