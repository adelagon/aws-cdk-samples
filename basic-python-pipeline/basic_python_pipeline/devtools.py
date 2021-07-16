from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecr as ecr,
    aws_codecommit as codecommit,
    core
)

class DevTools(core.Construct):

    @property
    def code_repo(self):
        return self._code_repo

    @property
    def ecr_repo(self):
        return self._ecr_repo

    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        ### CodeCommit - code repo
        self._code_repo = codecommit.Repository(
            self, "Repository",
            repository_name="flask-app",
            description="CodeCommit repo for the workshop")

        ### ECR - docker repo
        self._ecr_repo = ecr.Repository(
            self, "ECR",
            repository_name="flask-app",
            removal_policy=core.RemovalPolicy.DESTROY
        )