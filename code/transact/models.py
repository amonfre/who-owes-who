from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_slug
from django.db.models.signals import post_save
from common.util.analyze import Person,Optimizer

# Create your models here.

#class to add dates to all models
class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

#profile for keeping track of user information
class Profile(BaseModel):
  friends = models.ManyToManyField("self")
  user = models.ForeignKey(User,related_name='profile')
  description = models.TextField(default="")
  networth = models.IntegerField(default=0)
  

#this function creates a profile for the user when the user is created
#best way to extend djangos built in user model
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


class FriendRequest(BaseModel):
  sender = models.ForeignKey(User,related_name='friendor')
  recepient = models.ForeignKey(User,related_name='friendee')

  #runs our signature analytical algorithim
def analyze():
  CalculatedTransaction.objects.all().delete()
  users = User.objects.all()
  people = []
  uid = []
  for user in users:
    uid.append(user.id)
  for user in users:
    transacts = []
    friends = []
    for partner in users:
      #sent means assets to the current user, received = debt
      sent = Transaction.objects.filter(sender=user).filter(recepient=partner).filter(accepted=1)
      received = Transaction.objects.filter(sender=partner).filter(recepient=user).filter(accepted=1)
      netconnect = 0
      for trans in sent: 
        netconnect += trans.amount
      for trans in received:
        netconnect -= trans.amount

      if netconnect < 0:
        transacts.append((uid.index(partner.id),(-1)*netconnect))

    for friend in user.profile.get().friends.all():
      friends.append(uid.index(friend.id))

    people.append(Person(friends,transacts))

  solved = Optimizer(people).optimize()

  #process returned matrix
  rpos = -1
  
  for row in solved:
    rpos += 1
    cpos = -1
    for col in row:
      cpos += 1
      if col > 0:
        CalculatedTransaction.objects.create(sender=users[cpos],recepient=users[rpos],amount=col)

#sender is creditor, recepient is debtor, accepted is 0 for new request 1 if accepted
class Transaction(BaseModel):
<<<<<<< HEAD:code/transact/models.py
   created_at = models.DateField()
   #recepient = models.ForeignKey(User, related_name='recepient')
   recipient = models.CharField(max_length=100, default='')
   sender = models.ForeignKey(User, related_name='sender')
   amount = models.FloatField()
   pay = models.BooleanField(default=False)
=======
   recepient = models.ForeignKey(User,related_name='recepient')
   sender = models.ForeignKey(User,related_name='sender') 
   amount = models.FloatField()
   accepted = models.PositiveIntegerField(default=0)

#transactions after algorithim is run
class CalculatedTransaction(BaseModel):
  recepient = models.ForeignKey(User,related_name='recepientc')
  sender = models.ForeignKey(User,related_name='senderc')
  amount = models.FloatField()

#calculates networth for every user
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



#calculates networth and analyzes the graph after every transaction
def calculate_net_worth(sender, instance, created, **kwargs):
    analyze()
    update_net_worth(instance.sender.profile.get())
    update_net_worth(instance.recepient.profile.get())

post_save.connect(calculate_net_worth, sender=Transaction)

class TransactionRequest(BaseModel):
  sender = models.ForeignKey(User,related_name='tsender')
  recepient = models.ForeignKey(User,related_name='trecepient')
  transaction = models.ForeignKey(Transaction,related_name='request')
>>>>>>> 6e35611285de7198fac81d0e88a68f132b83f7d1:transact/models.py
   
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
<<<<<<< HEAD:code/transact/models.py
        exclude = ['sender']
        fields = ['recipient', 'amount', 'pay']
        
    
=======
        fields = ['amount']

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["description"]
      
>>>>>>> 6e35611285de7198fac81d0e88a68f132b83f7d1:transact/models.py
