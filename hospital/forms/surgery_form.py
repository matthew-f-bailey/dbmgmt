from django import forms
from hospital.models.actions import Surgery
from hospital.forms.base_form import BootstrapForm


class SurgeryForm(BootstrapForm):
    class Meta:
        model = Surgery
        fields = [
            'date',
            "surgeon",
            "nurse",
            "patient",
            "code",
            "anatomical_location",
            "category",
            "type",
            "special_needs",
        ]
