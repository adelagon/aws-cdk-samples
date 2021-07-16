from aws_cdk import (
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    core
)

class Tasks(core.Construct):

    @property
    def flask_app(self):
        return self._flask_app

    def __init__(self, scope: core.Construct, id: str, infra, devtools, **kwargs):
        super().__init__(scope, id, **kwargs)

        self._flask_app = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "FlaskApp",
            cluster=infra.cluster,
            cpu=512,
            memory_limit_mib=4096,
            desired_count=1,
            public_load_balancer=True,
            task_image_options={
                "image": ecs.ContainerImage.from_ecr_repository(devtools.ecr_repo, tag="latest"),
                "container_port": 5000,
                "container_name": "flask-app",
                "enable_logging": True
            }
        )

        ### Speed up deploy
        self._flask_app.target_group.set_attribute("deregistration_delay.timeout_seconds", "5")
        self._flask_app.target_group.configure_health_check(
            interval=core.Duration.seconds(5),
            timeout=core.Duration.seconds(4),
            healthy_threshold_count=2
        )