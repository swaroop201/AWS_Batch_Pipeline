import os
import json
import boto3
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

ses = boto3.client('ses')
glue = boto3.client('glue', region_name='us-east-1')

# Variables for the job: 
email_from = os.environ['email_from']
email_to = os.environ['email_to']
glue_crawler_name = os.environ['glue_crawler_name']

def lambda_handler(event, context):
    
    #print("Received event: " + json.dumps(event, indent=2))
    status = event['detail']['state']
    
    print("Status: " + str(status[0]))
    
    if status[0] == 'SUCCEEDED':
        email_subject = 'NSE Stock Price | Feed Processing - Successful'
    else:
        email_subject = 'NSE Stock Price | Feed Processing - Failed'
    email_body = ''
        
    response_ses = ses.send_email(
        Source = email_from,
        Destination={
            'ToAddresses': [
                email_to,
            ],
        },
        Message={
            'Subject': {
                'Data': email_subject
            },
            'Body': {
                'Text': {
                    'Data': email_body
                }
            }
        }
    )

    print("Glue Crawler: " + glue_crawler_name)
    
    response_glue = glue.start_crawler(Name=glue_crawler_name)
    logger.info('## STARTED GLUE CRAWLER: ' + glue_crawler_name)

    return response_ses
