from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Transaction(models.Model):
   created_at = models.DateField()
   recepient = models.ForeignKey(User,related_name='recepient')
   sender = models.ForeignKey(User,related_name='sender')
   amount = models.FloatField()
    

