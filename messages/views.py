from django.shortcuts import render
from .models import Lead, Message
from .serializers import LeadSerializer, MessageSerializer
import views


# Create your views here.

class LeadViewSet(views.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

class MessageViewSet(views.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = MessageSerializer