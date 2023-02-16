from aws_cdk import (
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_codebuild as codebuild,
    core as cdk
)

class GithubCodepiplineStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        pipeline = codepipeline.Pipeline(
            self, "Pipeline",
            pipeline_name="release-pipeline",
            stages=[]
        )

        pat = cdk.SecretValue(
            value="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"
        )
        source_output = codepipeline.Artifact()
        pipeline.add_stage(
            stage_name="Source",
            actions=[
                codepipeline_actions.GitHubSourceAction(
                    oauth_token=pat,
                    owner="alvinatorrr",
                    repo="codepipeline-integration",
                    action_name="GitHubCheckout",
                    output=source_output,
                    #trigger=codepipeline_actions.GitHubTrigger("POLL")
                )
            ]
        )

        build = codebuild.PipelineProject(
            self, "Build",
            project_name="codebuild-hello",
            build_spec=codebuild.BuildSpec.from_source_filename(
                filename="buildspec.yaml"
            ),
            environment=codebuild.BuildEnvironment(
                privileged=True,
                build_image=codebuild.LinuxBuildImage.AMAZON_LINUX_2_3
            ),
        )
        build_output = codepipeline.Artifact()
        pipeline.add_stage(
            stage_name="Build",
            actions=[
                codepipeline_actions.CodeBuildAction(
                    action_name="HelloAction",
                    input=source_output,
                    outputs=[build_output],
                    project=build
                )
            ]
        )

        