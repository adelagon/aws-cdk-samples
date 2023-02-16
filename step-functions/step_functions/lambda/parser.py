import os
import csv
import boto3
import json

def handler(event, context):
    s3 = boto3.resource(s3)
    os.chdir('/tmp')

    for record in context["Records"]:
        # Context Details
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
                print(row)