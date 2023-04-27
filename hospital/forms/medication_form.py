from django import forms
from hospital.models.illnesses import Medication, Interactions
from hospital.forms.base_form import BootstrapForm


class MedicationForm(BootstrapForm):
    class Meta:
        model = Medication
        fields = [
            'code',
            'name',
            'available_qnty',
            'cost',
            'usage'
        ]

    
class InteractionForm(BootstrapForm):
    medication1 = forms.ModelChoiceField(queryset= Medication.objects.all())
    medication2 = forms.ModelChoiceField(queryset= Medication.objects.all())
    class Meta:
        model = Interactions
        fields = [
            'medication1',
            'medication2',
            'severity'
        ]
        