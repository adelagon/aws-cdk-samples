from aws_cdk import core as cdk
from aws_cdk import core

from infra import Infra
from devtools import DevTools
from tasks import Tasks
from pipeline import Pipeline

class BasicPythonPipelineStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ### CDK Constructs for the Base Infra
        infra = Infra(self, "Infra")

        ### CDK Constructs for the DevTools
        devtools = DevTools(self, "DevTools")

        
        ### CDK Constructs for the Fargate Services
        tasks = None
        
        ### Enable the following lines once the Git Repository has been seeded
        #tasks = Tasks(self, "Tasks", infra, devtools)

        ### CDK Constructs for the Pipeline
        pipeline = Pipeline(self, "Pipeline", devtools, tasks)



