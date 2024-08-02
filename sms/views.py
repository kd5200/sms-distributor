from django.shortcuts import render
from .models import Lead, Message
from .serializers import LeadSerializer, MessageSerializer
from rest_framework import viewsets
import boto3
import os
from dotenv import load_dotenv

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
    client = boto3.client('sns', region_name=AWS_REGION_NAME)
    response = client.publish(
        PhoneNumber=phone_number,
        Message=message
    )

    return response