import boto3
import sys
from dateutil import parser
def lambda_handler(event, context):
    
    def newest_image(list_of_images):
        latest = None

        for image in list_of_images:
            if not latest:
               latest = image
               continue

            if parser.parse(image['CreationDate']) > parser.parse(latest['CreationDate']):
                latest = image

        return latest
    
    client = boto3.client('ec2', region_name='us-east-1')

    response = client.describe_images(Owners=['self'])
    source_image = newest_image(response['Images'])
    print(source_image['ImageId'])

#Copy AMI Code start from here    
    dest_region = boto3.client('ec2',region_name='ap-south-1')

    response = dest_region.copy_image( Name='test2', Description='Copied this AMI from region us-east-1', SourceImageId=source_image['ImageId'], SourceRegion='us-east-1')
    
    
    