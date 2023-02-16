from aws_cdk import (
    core as cdk,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_stepfunctions as stepfunctions,
    aws_stepfunctions_tasks as tasks
)

from aws_solutions_constructs.aws_s3_stepfunctions import S3ToStepfunctions, S3ToStepfunctionsProps

class StepFunctionsStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        parser_function = _lambda.Function(
            self,
            "ParserFunction",
            code=_lambda.Code.asset("step_functions/lambda"),
            handler='parser.handler',
            runtime=_lambda.Runtime.PYTHON_3_7
        )
        
        notify_failure_function = _lambda.Function(
            self,
            "NotifyErrorFunction",
            code=_lambda.Code.asset("step_functions/lambda"),
            handler='notify.failure_handler',
            runtime=_lambda.Runtime.PYTHON_3_7
        )

        notify_failure_task = tasks.LambdaInvoke(
            self,
            "NotifyFailure",
            lambda_function=notify_failure_function
        )

        parser_task = tasks.LambdaInvoke(
            self,
            "ParserTask",
            lambda_function=parser_function
        ).add_catch(notify_failure_task)

        state_machine=stepfunctions.StateMachineProps(
            definition=parser_task.next(
                stepfunctions.Succeed(self, "NotifyTask")
            )
        )
        
        # Trigger StepFunction for S3 Events
        S3ToStepfunctions(
            self,
            "Dropship",
            state_machine_props=state_machine
        )