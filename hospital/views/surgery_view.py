from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from hospital.forms.surgery_form import SurgeryForm
from hospital.models.actions import Surgery
from hospital.models.people import Nurse, Surgeon
from hospital.models.skill_types import SurgeryType


class SurgeryListView(ListView):
    """ Basic List View to show Surgery """

    # specify the model for list view
    model = Surgery

    def get_queryset(self, *args, **kwargs):
        """ Do any orders, filters, etc """
        qs = super(SurgeryListView, self).get_queryset(*args, **kwargs)
        # qs = qs.order_by("last_name")
        return qs

class SurgeryDetailView(DetailView):
    model = Surgery

class SurgeryCreateView(CreateView):
    model = Surgery
    form_class = SurgeryForm

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        surgeon = Surgeon.objects.get(emp_number=self.request.POST.get("surgeon"))
        nurse = Nurse.objects.get(emp_number=self.request.POST.get("nurse"))
        type = SurgeryType.objects.get(id=self.request.POST.get("type"))
        if surgeon.can_perform(type) and nurse.can_perform(type):
            return super().form_valid(form)

        # If one can't return the errors
        print("Cannot schedule surgery")
        if not surgeon.can_perform(type):
            form.add_error("surgeon" ,f"Surgeon cannot perform Surgery of type {type}. Surgeon's Skills: {surgeon.get_skills}")

        if not nurse.can_perform(type):
            form.add_error("nurse", f"Nurse cannot assist in Surgery of type {type}. Nurses Skills: {nurse.get_skills}")

        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('detail_surgery_view', kwargs={'pk': self.object.id})
