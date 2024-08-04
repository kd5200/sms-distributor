from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Lead, Message
from .views import send_sms, send_ses
import boto3
from moto import mock_sns, mock_ses

# Create your tests here.


class LeadAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.lead_url = '/api/leads/'
        self.message_url = '/api/messages/'
        self.lead_data = {'name': 'John Doe', 'email': 'john@example.com'}

    def test_create_lead(self):
        response = self.client.post(self.lead_url, self.lead_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lead.objects.count(), 1)
        self.assertEqual(Lead.objects.get().name, 'John Doe')

