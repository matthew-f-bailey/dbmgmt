from django.shortcuts import render
from django.urls import reverse
from hospital.forms.people_form import PatientForm


def create_patient_view(request):

    # Navigations to page
    if request.method == "GET":
        patient_form = PatientForm()
        return render(
            request,
            "create_form.html",
            {
                "model_form": patient_form,
                "post_to": reverse("create_patient_view")
            }
        )

    patient_form = PatientForm(request)

