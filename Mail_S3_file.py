
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):


    SENDER = "Nikhil Pawar <nikhil.pawar@blazeclan.com>"
    RECIPIENT = "aniket.pradhane@blazeclan.com"
    CONFIGURATION_SET = "ConfigSet"
    AWS_REGION = "us-east-1"
    SUBJECT = "Patching Update on Server"
    BODY_TEXT = (""
                )
    BODY_HTML = """<html>
                <head></head>
                <body>
                <h1>Patching Update on Server</h1>
                </body>
                </html>
                """            
    CHARSET = "UTF-8"
    client = boto3.client('ses',region_name=AWS_REGION)
    inbucket = 'aniketbucket'
    s3 = boto3.resource('s3')
#    outfile = io.StringIO()
    bucket = s3.Bucket(inbucket)
    alldata = ""
    for obj in bucket.objects.all():
        x = obj.get()['Body'].read().decode()
        alldata = alldata+x.strip()+"\n"+"-"*80+"\n"
       # OT = x
        
    print (alldata)
# Try to send the email.
    try:
    #Provide the contents of the email.
           response = client.send_email(
               Destination={
                    'ToAddresses': [
                        RECIPIENT,
                    ],
               },
               Message={
                   'Body': {
#                       'Html': {
#                           'Charset': CHARSET,
#                           'Data': alldata,
 #                      },
                       'Text': {
                           'Charset': CHARSET,
                           'Data': alldata,
                       },
                    },
                    'Subject': {
                         'Charset': CHARSET,
                         'Data': SUBJECT,
                    },
               },
               Source=SENDER,
            )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
        

