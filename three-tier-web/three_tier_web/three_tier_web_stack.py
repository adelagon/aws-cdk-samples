from aws_cdk import (
  core
)
from network_topology import NetworkTopology
from webservers import WebServers
from apiservers import APIServers
from database import Database
from load_balancer import LoadBalancer

class ThreeTierWebStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        topology = NetworkTopology(
          self, 'VPC'
        )

        webservers = WebServers(
          self, 'WebServers',
          vpc=topology.vpc,
          instance_type="t3.nano"
        )

        apiservers = APIServers(
          self, 'APIServers',
          vpc=topology.vpc,
          instance_type="t3.nano"
        )

        database = Database(
          self, 'Database',
          vpc=topology.vpc,
          master_username="alvinator",
          master_password="passw0rd",
          database_name="production"
        )

        load_balancer = LoadBalancer(
          self, 'LoadBalancer',
          vpc=topology.vpc,
          instances=webservers.instances
        )