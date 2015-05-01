from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from transact.models import Profile
from transact.models import ProfileForm
from transact.models import Transaction
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

@login_required
def index(request):
  return render(request,'index.html')

@login_required
def new_transaction(request):

  # if this is a POST request we need to process the form data
  if request.method == 'POST':
    # create a form instance and populate it with data from the request:
    form = TransactionForm(request.POST)
    # check whether it's valid:
    if form.is_valid():
      trans = form.save(commit = False)
      trans.created_at = timezone.now()
      tuser = User.objects.filter(username=form.cleaned_data['friend'])
      if tuser.first() == request.user:
        form.add_error("friend","Can't transact with yourself")
        return render(request, 'transact.html', {'form': form})

      if form.cleaned_data['lob'] == "loan":
        trans.recepient = tuser.first()
        trans.sender = request.user
      else:
        trans.recepient = request.user
        trans.sender = tuser.first()
      trans.save()
      form.save_m2m()
      TransactionRequest.objects.create(sender=request.user,recepient=tuser.first(),transaction=trans)
      return HttpResponseRedirect('/transact/transactions')

    # if a GET (or any other method) we'll create a blank form
  else:
      form = TransactionForm()

  return render(request, 'transact.html', {'form': form})

def profile(request):
  if request.method == 'POST':
      form = ProfileForm(data=request.POST,instance=request.user.profile.get())
      if form.is_valid():
        form.save()
        form = ProfileForm(instance=request.user.profile.get())
  else:
    form = ProfileForm(instance=request.user.profile.get())
  return render(request,"profile.html",{'form':form})

def transactions(request):
  allts = Transaction.objects.filter(Q(sender=request.user)|Q(recepient=request.user))
  pendingts = TransactionRequest.objects.filter(recepient=request.user)
  sentts = TransactionRequest.objects.filter(sender=request.user)
  acceptedts = allts.filter(accepted=1)      

  return render(request, 'transactions.html', {'acceptedts':acceptedts, 'pendingts':pendingts, 'sentts':sentts},context_instance=RequestContext(request))
  
def canceltransactionrequest(request):
  tr = TransactionRequest.objects.filter(id=request.GET.get('id','-1'))
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
    trans.accepted = 1
    trans.save()
    trr.delete()
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
        return render(request,'friends.html',{'myfriends':myfriends,'requests':requests,'myasks':myasks, 'form':form},context_instance=RequestContext(request))

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
    nodes.append({"name":user.username,"networth":user.profile.get().networth})
    uids.append(user.id)
  for trans in Transaction.objects.filter(accepted=1):
    links.append({"source":uids.index(trans.sender.id), "target":uids.index(trans.recepient.id)})
    
  return JsonResponse({"nodes":nodes,"links":links})

def visual(request):
  return render(request, 'visual.html')
# Create your views here.
