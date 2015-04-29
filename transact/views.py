from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from transact.models import Transaction
from transact.models import TransactionForm
from django.contrib.auth.models import User 
from django.http import JsonResponse

from django.http import HttpResponseRedirect

@login_required
def index(request):
  html = "t1est"
  return HttpResponse(html)

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
      #trans.sender = request.user.username
      trans.save()
      form.save_m2m()
      return HttpResponseRedirect('/transact/')

    # if a GET (or any other method) we'll create a blank form
  else:
      form = TransactionForm()

  return render(request, 'transact.html', {'form': form})

@login_required
def visualize_json(request):
  users = User.objects.all()
  nodes = []
  links = []
  uids = list(users.values_list('id', flat=True))
  for user in users:
    nodes.append({"name":user.username})
    for trans in Transaction.objects.filter(sender = user):
      links.append({"source":uids.index(trans.sender.id), "target":uids.index(trans.recipient.id)})
    
  return JsonResponse({"nodes":nodes,"links":links})
  
def visual(request):
  return render(request, 'visual.html')
# Create your views here.
