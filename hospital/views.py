from django.shortcuts import render
from .models.people import Physician, Patient, Nurse, Surgeon

# Create your views here.

def home(request):
    counts = {
        "physicians": Physician.objects.all(),
        "surgeons": Surgeon.objects.all(),
        "nurses": Nurse.objects.all(),
        "patients": Patient.objects.all(),
    }
    return render(request, 'home.html', counts)