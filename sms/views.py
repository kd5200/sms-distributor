from django.shortcuts import render
from .models import Lead, Message
from .serializers import LeadSerializer, MessageSerializer
from rest_framework import viewsets, status
import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import BotoCoreError, ClientError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, DjangoModelPermissionsOrAnonReadOnly



# Create your views here.

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION_NAME = os.getenv('AWS_REGION_NAME')



class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


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
@permission_classes([AllowAny])  # Use a permission class that doesn't require a queryset
def send_sms_view(request):
    phone_number = request.data.get('phone_number')
    message = request.data.get('message')
    if not phone_number or not message:
        return Response({"error": "Missing phone_number or message"}, status=status.HTTP_400_BAD_REQUEST)
    
    response = send_sms(phone_number, message)
    if response:
        return Response(response, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Failed to send SMS"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])  # Use a permission class that doesn't require a queryset
def send_email_view(request):
    to_address = request.data.get('to_address')
    subject = request.data.get('subject')
    body = request.data.get('body')
    if not to_address or not subject or not body:
        return Response({"error": "Missing to_address, subject, or body"}, status=status.HTTP_400_BAD_REQUEST)
    
    response = send_ses(to_address, subject, body)
    if response:
        return Response(response, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Failed to send email"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)