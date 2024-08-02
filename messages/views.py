from django.shortcuts import render
from .models import Lead, Message
from .serializers import LeadSerializer, MessageSerializer
from rest_framework import viewsets


# Create your views here.

class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = MessageSerializer