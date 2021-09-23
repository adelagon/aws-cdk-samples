import os
import csv
import boto3
import json

def handler(event, context):
    s3 = boto3.resource('s3')
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName=os.environ['QUEUE_NAME'])

    os.chdir('/tmp')

    for record in event["Records"]:
        # Event Details
        object_key = record["s3"]["object"]["key"]
        bucket_name = record["s3"]["bucket"]["name"]
        file_name = object_key.split('/')[-1]
        bucket = s3.Bucket(bucket_name)

        # Download the csv file
        print("Downloading csv file: {}".format(file_name))
        bucket.download_file(
            object_key,
            file_name
        )

        # Parse the object
        with open(file_name, encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Send entries into queue for processing
                print("Sending Task: {} to queue.".format(row))
                response = queue.send_message(MessageBody=json.dumps(row))
                print("Task Queued: {}".format(response.get('MessageId')))

        # Upload the processed csv into S3 into 'processed' folder
        # delete from 'input' folder
        csvfile.close()
        s3.upload_file(
            file_name,
            "processed/{}".format(file_name)
        )
        s3.delete_objects(
            Delete={
                'Objects': [
                    {
                        'Key': object_key
                    }
                ]
            }
        )
            