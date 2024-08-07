from django.shortcuts import render
from .models import Lead, Message
from .serializers import LeadSerializer, MessageSerializer
from rest_framework import viewsets
import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import BotoCoreError, ClientError
from rest_framework.decorators import api_view
from rest_framework.response import Response



# Create your views here.

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION_NAME = os.getenv('AWS_REGION_NAME')



class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = MessageSerializer


def send_sms(phone_number, message):
    client = boto3.client(
        'sns',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION_NAME
    )
    try:
        response = client.publish(
            PhoneNumber=phone_number,
            Message=message
        )
    except (BotoCoreError, ClientError) as error:
        print(f"Failed to send SMS: {error}")
        response = None

    return response

def send_ses(to_address, subject, body):
    client = boto3.client(
        'ses',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION_NAME
    )
    try:
        response = client.send_email(
            Source='daviskareem92@gmail.com',
            Destination={'ToAddresses': [to_address]},
            Message={
                'Subject': {'Data': subject},
                'Body': {'Text': {'Data': body}}
            }
        )
    except (BotoCoreError, ClientError) as error:
        print(f"Failed to send email: {error}")
        response = None

    return response

# Keep in mind, when moving into production that we need to request to be removed from the sandbox environment within the AWS console for SES for daily limit increases and sending marketing messages to unverified recepients. 


@api_view(['POST'])
def send_sms_view(request):
    phone_number = request.data.get('phone_number')
    message = request.data.get('message')
    response = send_sms(phone_number, message)
    return Response(response)

@api_view(['POST'])
def send_email_view(request):
    to_address = request.data.get('to_address')
    subject = request.data.get('subject')
    body = request.data.get('body')
    response = send_ses(to_address, subject, body)
    return Response(response)