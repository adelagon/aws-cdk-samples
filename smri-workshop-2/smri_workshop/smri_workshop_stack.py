from constructs import Construct
from aws_cdk.aws_events import (
    Rule,
    Schedule
)
from aws_cdk import (
    aws_events_targets as targets
)
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw
)

from .hitcounter import HitCounter

class SmriWorkshopStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # API Handler
        api_fn = _lambda.Function(
            self, 'API',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset('lambda'),
            handler='api_fn.handler',
        )
        
        # Hit Counter
        api_fn_counter = HitCounter(
            self, "HelloHitCounter",
            downstream=api_fn
        )
        
        # API Endpoint 
        apigw.LambdaRestApi(
            self, "APIEndpoint",
            handler=api_fn_counter._handler
        )
        
        # Check Status Handler
        check_status_fn = _lambda.Function(
            self, 'CheckStatus',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset('lambda'),
            handler='check_status_fn.handler',
        )
        
        # Run Check Status every minute
        rule = Rule(self, "ScheduleRule",
            schedule=Schedule.cron(minute="0/1"),
        )
        
        rule.add_target(
            targets.LambdaFunction(
                check_status_fn,
                retry_attempts=2
            )
        )