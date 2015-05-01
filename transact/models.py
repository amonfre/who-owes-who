from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_slug
from django.db.models.signals import post_save

# Create your models here.

class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Profile(BaseModel):
  friends = models.ManyToManyField("self")
  user = models.ForeignKey(User,related_name='profile')
  description = models.TextField(default="")
  networth = models.IntegerField(default=0)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


class FriendRequest(BaseModel):
  sender = models.ForeignKey(User,related_name='friendor')
  recepient = models.ForeignKey(User,related_name='friendee')


  
class Transaction(BaseModel):
   created_at = models.DateField()
   recepient = models.ForeignKey(User,related_name='recepient')
   sender = models.ForeignKey(User,related_name='sender')
   amount = models.FloatField()
   accepted = models.PositiveIntegerField(default=0)

def update_net_worth(prof):
  user = prof.user
  assets = Transaction.objects.filter(sender=user).filter(accepted=1)
  debts = Transaction.objects.filter(recepient=user).filter(accepted=1)
  nw = 0
  for asset in assets:
    nw += asset.amount
  for debt in debts:
    nw -= debt.amount
  prof.networth = nw
  prof.save()

def calculate_net_worth(sender, instance, created, **kwargs):
    update_net_worth(instance.sender.profile.get())
    update_net_worth(instance.recepient.profile.get())

post_save.connect(calculate_net_worth, sender=Transaction)

class TransactionRequest(BaseModel):
  sender = models.ForeignKey(User,related_name='tsender')
  recepient = models.ForeignKey(User,related_name='trecepient')
  transaction = models.ForeignKey(Transaction,related_name='request')

   
class TransactionForm(ModelForm):
    def validate_friend(value):
      users = User.objects.filter(username=value)
      if not users.exists():
        raise ValidationError("User does not exist")
      
    friend = forms.CharField(label='Friend',validators=[validate_slug,validate_friend])
    CHOICES=[('loan','Loan'),
         ('borrow','Borrow')]
    lob = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
    class Meta:
        model = Transaction
        fields = ['amount']

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["description"]
      
