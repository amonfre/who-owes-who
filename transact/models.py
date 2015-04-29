from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm

# Create your models here.

class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Transaction(BaseModel):
   created_at = models.DateField()
   #recepient = models.ForeignKey(User, related_name='recepient')
   recipient = models.CharField(max_length=100)
   sender = models.ForeignKey(User,related_name='sender')
   amount = models.FloatField()
   
class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['recipient', 'sender', 'amount']
        
    
