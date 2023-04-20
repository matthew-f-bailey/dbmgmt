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

# Overide label function to show medication name and code in dropdown
class InteractionModelChoice(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.name}, {obj.code}'
    
class InteractionForm(BootstrapForm):
    medication1 = InteractionModelChoice(queryset= Medication.objects.all())
    medication2 = InteractionModelChoice(queryset= Medication.objects.all())
    class Meta:
        model = Interactions
        fields = [
            'medication1',
            'medication2',
            'severity'
        ]
        