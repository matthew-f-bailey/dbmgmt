from django import forms
from hospital.models.places import Bed
from hospital.forms.base_form import BootstrapForm


class BedForm(BootstrapForm):
    class Meta:
        model = Bed
        fields = [
            'bed_letter',
            'room',
        ]
