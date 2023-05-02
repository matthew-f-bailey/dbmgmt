from django import forms
from hospital.models.skill_types import AssignedSkills
from hospital.forms.base_form import BootstrapForm


class AssignedSkillsForm(BootstrapForm):
    class Meta:
        model = AssignedSkills
        fields = [
            'person',
            'skill',
        ]
