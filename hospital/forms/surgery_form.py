from django import forms
from hospital.models.actions import Surgery
from hospital.forms.base_form import BootstrapForm
from hospital.models.people import Nurse, Surgeon
from hospital.models.skill_types import SurgeryType


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

    # def clean(self):
    #     surgeon = Surgeon.objects.get(emp_number=self.cleaned_data.get("surgeon"))
    #     nurse = Nurse.objects.get(emp_number=self.cleaned_data.get("nurse"))
    #     type = SurgeryType.objects.get(id=self.cleaned_data.get("type"))
    #     if not surgeon.can_perform(type) or not nurse.can_perform(type):
    #         raise forms.ValidationError("CANNOT PERFORM")