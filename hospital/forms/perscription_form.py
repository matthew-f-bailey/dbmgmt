from django import forms
from hospital.models.actions import Perscriptions
from hospital.forms.base_form import BootstrapForm


class PerscriptionForm(BootstrapForm):
    class Meta:
        model = Perscriptions
        fields = [
            'physician',
            "patient",
            "medication",
            "frequency",
            "dosage",
        ]
