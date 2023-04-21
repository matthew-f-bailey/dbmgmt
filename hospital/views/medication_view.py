from django.shortcuts import render
from django.urls import reverse
from hospital.forms.medication_form import MedicationForm, InteractionForm
from django.shortcuts import redirect, render
from django.contrib import messages

# To add a new medication
def create_medication_view(request):
    if request.method == "GET":
        medication_form = MedicationForm()
        return render(
            request,
            "create_form.html",
            {
                "header" : "Create Medication",
                "model_form": medication_form,
                "post_to": reverse("create_medication_view")
            }
        )

    elif request.method == "POST":
        medication_form = MedicationForm(request.POST)
        if medication_form.is_valid():
            medication_form.save()
            print(medication_form)
            # Once a medication is created redirect to medicatoin interacion page
            return redirect("create_medication_interaction")

# To add interaction between medications
def create_medication_interaction(request):
    if request.method == "GET":
        interaction_form = InteractionForm()
        return render(
            request,
            "create_form.html",
            {
                "header" : "Add Medication Interactions",
                "model_form": interaction_form,
                "post_to": reverse("create_medication_interaction")
            }
        )
    elif request.method == "POST":
        interaction_form = InteractionForm(request.POST)
        if interaction_form.is_valid():
            print (interaction_form.data)
            # Check if the same mediciation is selected
            if (interaction_form.data.get('medication1') == interaction_form.data.get('medication2')):
                messages.error(request, "Can't assign interaction between the same medicine")
            else:
                interaction_form.save()
            return redirect("create_medication_interaction")
        # If interaction already exist return a message and redirct to the same page
        else:
            messages.error(request, 'This interaction already exists')
            return redirect("create_medication_interaction")


