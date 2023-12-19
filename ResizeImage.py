import traceback
import boto3
from io import BytesIO
from PIL import Image, ImageOps, ExifTags
from botocore.exceptions import ClientError


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

# Method 1:
    # try:
    #     img = Image.open(BytesIO(file_byte))
    #     format = img.format
    #     if hasattr(img, '_getexif'): # only present in JPEGs
    #         for orientation in ExifTags.TAGS.keys(): 
    #             if ExifTags.TAGS[orientation]=='Orientation':
    #                 break 
    #         e = img._getexif()       # returns None if no EXIF data
    #         if e is not None:
    #             exif=dict(e.items())
    #             orientation = exif[orientation] 

    #             if orientation == 3:   img = img.transpose(Image.ROTATE_180)
    #             elif orientation == 6: img = img.transpose(Image.ROTATE_270)
    #             elif orientation == 8: img = img.transpose(Image.ROTATE_90)

    #     img.thumbnail(size, Image.LANCZOS)
    #     img.save(file, format=format, optimize=True)
    #     content = file.getvalue()

    # except:
    #     traceback.print_exc()


# Method 2:
    try :
        img = Image.open(BytesIO(file_byte))
        if img.format in ('jpg','jpeg', 'JPG', 'JPEG'):
            ImageOps.exif_transpose(img, in_place=True)

        img.thumbnail(size, Image.LANCZOS)
        img.save(file, format=img.format, optimize=True)
        content = file.getvalue()

    except:
        traceback.print_exc()
    
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


    file.close()

    

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        print(f'Hold tight, resizing {bucket}/{key}...')
    
        resize_image(src_bucket=bucket, key=key, des_bucket=destBucket)



