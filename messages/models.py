from django.db import models

# Create your models here.


class Lead(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    subscribed = models.BooleanField(default=True)

class Message(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
