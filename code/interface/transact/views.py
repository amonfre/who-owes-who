#some code based off of django documentation

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from transact.models import Profile
from transact.models import ProfileForm
from transact.models import Transaction
from transact.models import CalculatedTransaction
from transact.models import TransactionForm
from transact.models import TransactionRequest
from transact.models import FriendRequest
from django.contrib.auth.models import User 
from django.http import JsonResponse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.template import RequestContext
from django import forms
import string
import random
from common.util.analyze import Person,GreedyOptimizer
from common.util.friendlyanalyze import FriendlyOptimizer
import time

@login_required
def index(request):
  networth = request.user.profile.get().networth
  if networth > 0:
    computations = CalculatedTransaction.objects.filter(sender=request.user)
  elif networth < 0:
    computations = CalculatedTransaction.objects.filter(recepient=request.user)
  else:
    computations = ""
  return render(request,'index.html',{ 'networth':networth,'computations':computations})

@login_required
def new_transaction(request):
  if request.method == 'POST':
    form = TransactionForm(request.POST)
    if form.is_valid():
      trans = form.save(commit = False)
      tuser = User.objects.filter(username=form.cleaned_data['friend'])
      if tuser.first() == request.user:
        form.add_error("friend","Can't transact with yourself")
        return render(request, 'transact.html', {'form': form})

      #decide whether the current user is borrowing or loaning money
      if form.cleaned_data['lob'] == "loan":
        trans.recepient = tuser.first()
        trans.sender = request.user
      else:
        trans.recepient = request.user
        trans.sender = tuser.first()
      trans.save()

      #we must save the manytomany relationships seperatly!
      form.save_m2m()

      #create a transactionrequest pending approval
      TransactionRequest.objects.create(sender=request.user,recepient=tuser.first(),transaction=trans)
      return HttpResponseRedirect('/transact/transactions')

  else:
      form = TransactionForm()

  return render(request, 'transact.html', {'form': form})

@login_required
def profile(request):
  if request.method == 'POST':
      form = ProfileForm(data=request.POST,instance=request.user.profile.get())
      if form.is_valid():
        form.save()
        form = ProfileForm(instance=request.user.profile.get())
  else:
    form = ProfileForm(instance=request.user.profile.get())
  return render(request,"profile.html",{'form':form})

@login_required
def transactions(request):
  pendingts = TransactionRequest.objects.filter(recepient=request.user)
  sentts = TransactionRequest.objects.filter(sender=request.user)
  acceptedts = Transaction.objects.filter(Q(sender=request.user)|Q(recepient=request.user)).filter(accepted=1)      

  return render(request, 'transactions.html', {'acceptedts':acceptedts, 'pendingts':pendingts, 'sentts':sentts},context_instance=RequestContext(request))
  
@login_required
def canceltransactionrequest(request):
  tr = TransactionRequest.objects.filter(id=request.GET.get('id','-1'))

  #check if user maliciously changed get request
  if not tr.exists():
    messages.add_message(request, messages.WARNING, 'Error')
    return HttpResponseRedirect('transactions')

  trr = tr.first()
  if not (trr.sender == request.user):
    messages.add_message(request, messages.WARNING, 'Error')
    return HttpResponseRedirect('transactions')
  
  trr.transaction.delete()
  trr.delete()
  
  return HttpResponseRedirect('transactions')

@login_required
def respond(request):
  tr = TransactionRequest.objects.filter(id=request.GET.get('id','-1'))
  if not tr.exists():
    messages.add_message(request, messages.WARNING, 'Error')
    return HttpResponseRedirect('transactions')
  trr = tr.first()
  if not (trr.recepient == request.user):
    messages.add_message(request, messages.WARNING, 'Error')
    return HttpResponseRedirect('transactions')

  if request.GET.get('c','-1') == "accept":
    trans = trr.transaction
    #mark as accepted
    trans.accepted = 1
    trans.save()
    trr.delete()
    #have users friend eachother and check if friendrequests exist and clear them 
    if not trr.recepient.profile.get().friends.filter(id=trr.sender.profile.get().id).exists():
        posssend = FriendRequest.objects.filter(sender=trr.sender).filter(recepient=trr.recepient)
        possrecep = FriendRequest.objects.filter(sender=trr.recepient).filter(recepient=trr.sender)
        if posssend.exists():
          posssend.get().delete()
        if possrecep.exists():
          possrecep.get().delete()
        trr.recepient.profile.get().friends.add(trr.sender.profile.get())

  elif request.GET.get('c','-1') == "reject":
    trr.transaction.delete()
    trr.delete()
  else:
    messages.add_message(request, messages.WARNING, 'Error')
  
  return HttpResponseRedirect('transactions')

class NewFriendForm(forms.Form):
  username = forms.CharField(label='Username:')

@login_required
def friends(request):
  myfriends = request.user.profile.get().friends
  requests = request.user.friendee
  myasks = request.user.friendor
  
  if request.method == 'POST':
    form = NewFriendForm(request.POST)
    if form.is_valid():
      usern = form.cleaned_data['username']
      friend = User.objects.filter(username=usern)
      if friend.first() == request.user:
        form.add_error("username","Can't friend yourself")
        return render(request,'friends.html', {'myfriends':myfriends,'requests':requests,'myasks':myasks, 'form':form},context_instance=RequestContext(request))

      if friend.exists():
        if not request.user.profile.get().friends.filter(id=friend.get().profile.get().id).exists():
          posssend = FriendRequest.objects.filter(sender=request.user).filter(recepient=friend.get()).exists()
          possrecep = FriendRequest.objects.filter(sender=friend.get()).filter(recepient=request.user).exists()
          if not (posssend or possrecep):
              
            FriendRequest.objects.create(sender = request.user, recepient=friend.get())
            form = NewFriendForm()
          else:
            form.add_error('username', "Pending request already")
        else:
          form.add_error('username', "Already friends")
      else:
        form.add_error('username', "User doesn't exist")
      

  else:
      form = NewFriendForm()
    
  return render(request,'friends.html',{'myfriends':myfriends,'requests':requests,'myasks':myasks, 'form':form},context_instance=RequestContext(request))

@login_required
def cancelfriendrequest(request):
    frr = FriendRequest.objects.filter(id=request.GET.get('id','-1'))
    if not frr.exists():
      messages.add_message(request, messages.WARNING, 'Error')
      return HttpResponseRedirect('friends')
    fr = frr.first()
    if not (fr.sender == request.user):
      messages.add_message(request, messages.WARNING, 'Error')
      return HttpResponseRedirect('friends')
    fr.delete()
    return HttpResponseRedirect('friends')
 
@login_required   
def processfriendship(request):
  frr = FriendRequest.objects.filter(id=request.GET.get('id','-1'))
  if not frr.exists():
    messages.add_message(request, messages.WARNING, 'Error')
    return HttpResponseRedirect('friends')
  fr = frr.first()
  if not (fr.recepient == request.user):
    messages.add_message(request, messages.WARNING, 'Error')
    return HttpResponseRedirect('friends')
  if request.GET.get('c','-1') == "accept":
    friends = request.user.profile.get().friends
    friends.add(fr.sender.profile.get())
    fr.delete()
  elif request.GET.get('c','-1') == "reject":
    fr.delete()
  else:
    messages.add_message(request, messages.WARNING, 'Error')
  
  return HttpResponseRedirect('friends')

@login_required
def visualize_json(request):
  users = User.objects.all()
  nodes = []
  links = []
  uids = []
  for user in users:
    #build nodes for graph
    nodes.append({"name":user.username,"networth":user.profile.get().networth})
    #keep uids so we can look up the order to provide the proper data for the js library
    uids.append(user.id)

  #build links  
  for trans in Transaction.objects.filter(accepted=1):
    links.append({"source":uids.index(trans.sender.id), "target":uids.index(trans.recepient.id)})
    
  return JsonResponse({"nodes":nodes,"links":links})

@login_required
def visual(request):
  return render(request, 'visual.html')

#see visualize_json
@login_required
def cvisualize_json(request):
  users = User.objects.all()
  nodes = []
  links = []
  uids = []
  for user in users:
    nodes.append({"name":user.username,"networth":user.profile.get().networth})
    uids.append(user.id)
  for trans in CalculatedTransaction.objects.all():
    links.append({"source":uids.index(trans.sender.id), "target":uids.index(trans.recepient.id)})
    
  return JsonResponse({"nodes":nodes,"links":links})

@login_required
def cvisual(request):
  return render(request, 'cvisual.html')

#makes a simple set of transactions where one user gives two users two dollars each who then give a fourth user 10 dollars each
#the algorithm should bypass the two users inbetween the fourth and first user

def createUsers(num):
  users = []
  for i in range(num):
    name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
    users.append(User.objects.create(username=name,password=name))

  return users


def createGroup():
  users = createUsers(10)
  for user in users:
    for user2 in users:
      if not user.profile.get().friends.filter(id=user2.profile.get().id).exists():
        user.profile.get().friends.add(user2.profile.get())
  for user in users:
    for i in range(5):
      other = random.choice(users)
      if random.random() > .5:
        Transaction(sender=user,recepient=other,amount=random.randint(0,100),accepted=1).save()
      else:
        Transaction(sender=other,recepient=user,amount=random.randint(0,100),accepted=1).save()
  return users[0]

@login_required
def createGroups(request):
  group1 = createGroup()
  group2 = createGroup()
  group3 = createGroup()
  group4 = createGroup()
  group5 = createGroup()

  Transaction(sender=group1,recepient=group2,amount=random.randint(0,100),accepted=1).save()
  Transaction(sender=group2,recepient=group3,amount=random.randint(0,100),accepted=1).save()
  Transaction(sender=group3,recepient=group4,amount=random.randint(0,100),accepted=1).save()
  Transaction(sender=group4,recepient=group5,amount=random.randint(0,100),accepted=1).save()
  Transaction(sender=group5,recepient=group1,amount=random.randint(0,100),accepted=1).save()

  return HttpResponseRedirect("control")

@login_required
def createSampleTransactions(request):
  us = createUsers(20)

  for user in us:
    for i in range(5):
      other = random.choice(us)
      if random.random() > .5:
        Transaction(sender=user,recepient=other,amount=random.randint(0,100),accepted=1).save()
      else:
        Transaction(sender=other,recepient=user,amount=random.randint(0,100),accepted=1).save()
      if  not user.profile.get().friends.filter(id=other.profile.get().id).exists():
        user.profile.get().friends.add(other.profile.get())
  return HttpResponseRedirect("control")


@login_required
def clean(request):
  Transaction.objects.all().delete()
  TransactionRequest.objects.all().delete()
  FriendRequest.objects.all().delete()
  for user in User.objects.all():
    if not user == request.user:
      if user.profile.exists():
        user.profile.get().delete()
      user.delete()
  prof = request.user.profile.get()
  prof.networth = 0
  prof.save()
  return HttpResponseRedirect("control")

@login_required
def smallCreateTransactions(request):

  r1 = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
  r2 = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
  r3 = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
  r4 = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))

  a = User.objects.create(username=r1,password="pass")
  b = User.objects.create(username=r2,password="pass")
  c = User.objects.create(username=r3,password="pass")
  d = User.objects.create(username=r4,password="pass")

  Transaction(sender=a,recepient=b,amount=10,accepted=1).save()
  Transaction(sender=a,recepient=c,amount=10,accepted=1).save()
  Transaction(sender=b,recepient=d,amount=10,accepted=1).save()
  Transaction(sender=c,recepient=d,amount=10,accepted=1).save()

  Profile.objects.filter(user=a).get().friends.add(b.profile.get())
  Profile.objects.filter(user=a).get().friends.add(c.profile.get())
  Profile.objects.filter(user=b).get().friends.add(d.profile.get())
  Profile.objects.filter(user=c).get().friends.add(d.profile.get())
  return HttpResponseRedirect("control")

@login_required
def control(request):
  return render(request,"control.html")

@login_required
def analyze_friendly(request):
  analyze(FriendlyOptimizer)
  return HttpResponseRedirect('control')

@login_required
def analyze_greedy(request):
  analyze(GreedyOptimizer)
  return HttpResponseRedirect('control')

  #runs our signature analytical algorithim
def analyze(optimizer):
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

  solved = optimizer(people).optimize()

  #process returned matrix
  rpos = -1
  
  for row in solved:
    rpos += 1
    cpos = -1
    for col in row:
      cpos += 1
      if col > 0:
        CalculatedTransaction.objects.create(sender=users[cpos],recepient=users[rpos],amount=col)