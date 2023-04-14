from django.shortcuts import render
from hospital.forms.people_form import PatientForm


def create_patient_view(request):
    patient_form = PatientForm()
    return render(request, "create_patient.html", {"patient_form": patient_form})