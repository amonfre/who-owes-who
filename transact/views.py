from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def index(request):
  html = "t1est"
  return HttpResponse(html)
# Create your views here.
