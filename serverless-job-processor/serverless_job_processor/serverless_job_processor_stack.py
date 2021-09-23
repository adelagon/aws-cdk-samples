import os
from aws_cdk import (
    core as cdk,
    aws_s3 as s3,
    aws_s3_deployment as s3_deploy,
    aws_lambda as _lambda,
    aws_sqs as sqs
)

from aws_cdk.aws_lambda_event_sources import (
    S3EventSource as s3_event,
    SqsEventSource as sqs_event
)

dirname = os.path.dirname(__file__)

class ServerlessJobProcessorStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ### SQS Queue
        queue = sqs.Queue(
            self,
            "JobQueue"
        )

        ### S3 Bucket
        bucket = s3.Bucket(
            self,
            "DropBucket"
        )

        ### Create input folder on S3 Bucket
        s3_deploy.BucketDeployment(
            self,
            "BucketDeploymentInputs",
            sources=[s3_deploy.Source.asset(os.path.join(dirname, "input"))],
            destination_bucket=bucket,
            destination_key_prefix="input"
        )

        ### Create processed folder on S3 Bucket
        s3_deploy.BucketDeployment(
            self,
            "BucketDeploymentProcessed",
            sources=[s3_deploy.Source.asset(os.path.join(dirname, "processed"))],
            destination_bucket=bucket,
            destination_key_prefix="processed"
        )

        ### Create failed folder on S3 Bucket
        s3_deploy.BucketDeployment(
            self,
            "BucketDeploymentFailed",
            sources=[s3_deploy.Source.asset(os.path.join(dirname, "failed"))],
            destination_bucket=bucket,
            destination_key_prefix="failed"
        )

        ### Lambda Functions
        parser_function = _lambda.Function(
            self,
            "ParserFunction",
            code=_lambda.Code.asset(os.path.join(dirname, "lambda")),
            handler='parser.handler',
            runtime=_lambda.Runtime.PYTHON_3_8
        )
        ## Listen to S3 events
        parser_function.add_event_source(
            s3_event(
                bucket,
                events=[s3.EventType.OBJECT_CREATED],
                filters=[s3.NotificationKeyFilter(prefix="input/", suffix=".csv")]
            )
        )
        ## Grant Read/Write to S3 Bucket
        bucket.grant_read_write(parser_function)
        ## Grant SQS Send access
        queue.grant_send_messages(parser_function)
        ## Provide Queue Name to function
        parser_function.add_environment("QUEUE_NAME", queue.queue_name)

        worker_function = _lambda.Function(
            self,
            "WorkerFunction",
            code=_lambda.Code.asset(os.path.join(dirname, "lambda")),
            handler='worker.handler',
            runtime=_lambda.Runtime.PYTHON_3_8
        )
        ## Listen to SQS events
        worker_function.add_event_source(
            sqs_event(
                queue
            )
        )