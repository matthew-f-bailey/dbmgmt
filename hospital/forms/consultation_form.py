from django import forms
from hospital.models.actions import Consultation
from hospital.forms.base_form import BootstrapForm


class ConsultationForm(BootstrapForm):
    class Meta:
        model = Consultation
        fields = [
            'physician',
            'patient',
            'date',
        ]
