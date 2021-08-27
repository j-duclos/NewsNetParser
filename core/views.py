from django.shortcuts import render
from . import views
from django.http import HttpResponse


# Create your views here.
def index(request):
    return HttpResponse('Hello Core!')