import boto3
import os
import sys
import pathlib
from io import BytesIO
from PIL import Image
from botocore.exceptions import ClientError
import PIL.Image

s3 = boto3.resource('s3')

destBucket = 'opencoach-thumbnails'

def resize_image(src_bucket, key, des_bucket):
    size = 500,500
    file = BytesIO()
    client = boto3.client('s3')
    
    try:
        file_byte = client.get_object(Bucket=src_bucket,Key= key)['Body'].read()

    except ClientError as e:
        if e.response['Error']['Code'] == 'AccessDenied':
            print("Lamda needs IAM permissions")

        else:
            print("Unexpected error: %s" % e)


    img = Image.open(BytesIO(file_byte))
    img.thumbnail(size, Image.LANCZOS)
    img.save(file, format=img.format, optimize=True)
    content = file.getvalue()
    
    try:
        response = client.put_object(
                Body=content,
                Bucket=des_bucket,
                Key= 'resized_' + key
                )
        
        print(f'Successfully resized and moved {key} from {src_bucket} to {des_bucket}')

    except ClientError as e:
        if e.response['Error']['Code'] == 'AccessDenied':
            print("Lamda needs IAM permissions")

        else:
            print("Unexpected error: %s" % e)

    

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
    
        resize_image(src_bucket=bucket, key=key, des_bucket=destBucket)



