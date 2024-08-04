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


class MessageAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.message_data = {'content': 'Test message'}

    def test_create_message(self):
        response = self.client.post(self.message_url, self.message_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Message.objects.get().content, 'Test message')

class NotificationTestCase(TestCase):
    @mock_sns
    def test_send_sms(self):
        phone_number = '+1234567890'
        message = 'Hello World'
        response = send_sms(phone_number, message)
        self.assertIsNotNone(response)
        self.assertIn('MessageId', response)

    @mock_ses
    def test_send_ses(self):
        to_address = 'recipient@example.com'
        subject = 'Test Email'
        body = 'This is a test email.'
        response = send_ses(to_address, subject, body)
        self.assertIsNotNone(response)
        self.assertIn('MessageId', response)