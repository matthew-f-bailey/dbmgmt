from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.urls import reverse
from django.views.generic.edit import CreateView

from hospital.models.skill_types import AssignedSkills
from hospital.forms.skill_form import AssignedSkillsForm
from hospital.models.people import Nurse, Surgeon


class AssignedSkillCreateView(CreateView):
    """ Basic List View to show patients """

    # specify the model for list view
    def get_initial(self) -> Dict[str, Any]:
        number = self.kwargs.get("pk")
        emp = Nurse.objects.filter(emp_number=number).first()
        if emp is None:
            emp = Surgeon.objects.get(emp_number=number)

        return {"person": emp.emp_number}

    model = AssignedSkills
    form_class = AssignedSkillsForm

    def get_success_url(self):
        number = self.request.POST.get("person")
        emp = Nurse.objects.filter(emp_number=number).first()
        if emp is None:
            # Then its a surgeon
            return reverse('detail_surgeon_view', kwargs={'pk': number})

        return reverse('detail_nurse_view', kwargs={'pk': number})



