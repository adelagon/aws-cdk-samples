from aws_cdk import (
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_codebuild as codebuild,
    core
)

class Pipeline(core.Construct):

    def __init__(self, scope: core.Construct, id: str, devtools, tasks, **kwargs):
        super().__init__(scope, id, **kwargs)

        ### CodePipeline
        pipeline = codepipeline.Pipeline(
            self, "Pipeline",
            pipeline_name="release-pipeline",
            stages=[]
        )

        ### Source Stage
        source_output = codepipeline.Artifact()
        pipeline.add_stage(
            stage_name="CheckoutSource",
            actions=[
                codepipeline_actions.CodeCommitSourceAction(
                    action_name="CodeCommit",
                    repository=devtools.code_repo,
                    output=source_output
                )
            ]
        )

        ### Build Docker Image Stage
        build_output = codepipeline.Artifact()
        ## CodeBuild Project
        docker = codebuild.PipelineProject(
            self, "DockerBuild",
            project_name="codebuild-docker-project",
            build_spec=codebuild.BuildSpec.from_source_filename(
                filename="docker_buildspec.yaml"
            ),
            environment=codebuild.BuildEnvironment(
                privileged=True,
                build_image=codebuild.LinuxBuildImage.AMAZON_LINUX_2_3
            ),
            environment_variables={
                "ECR_REPO_URI": codebuild.BuildEnvironmentVariable(
                    value=devtools.ecr_repo.repository_uri
                )
            },
            description="Docker Build Project",
            timeout=core.Duration.minutes(60)
        ) 
        # Allow CodeBuild Project rights to ECR repo
        devtools.ecr_repo.grant_pull_push(docker)
        ## Add CodeBuild Project to Pipeline
        pipeline.add_stage(
            stage_name="BuildImage",
            actions=[
                codepipeline_actions.CodeBuildAction(
                    action_name="DockerBuildImage",
                    input=source_output,
                    outputs=[build_output],
                    project=docker
                )
            ]
        )

        ### Deploy Staging Environment Stage
        if tasks:
            pipeline.add_stage(
                stage_name="DeployToStaging",
                actions=[
                    codepipeline_actions.EcsDeployAction(
                        action_name="DeployToStaging",
                        input=build_output,
                        service=tasks.flask_app.service,
                        deployment_timeout=core.Duration.minutes(60)
                    )
                ]
            )
        