from django.shortcuts import render
from .models.places import *

# Create your views here.

def home(request):
    context = {'clinic': Clinic.objects.first }
    return render(request, 'home.html', context)