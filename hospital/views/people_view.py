from typing import Any, Dict
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from hospital.forms.people_form import PatientForm
from hospital.models.people import Patient

class PatientListView(ListView):
    """ Basic List View to show patients """

    # specify the model for list view
    model = Patient

    def get_queryset(self, *args, **kwargs):
        """ Do any orders, filters, etc """
        qs = super(PatientListView, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("last_name")
        return qs

class PatientDetailView(DetailView):
    model = Patient

    def get_context_data(self, **kwargs):
        """ To disply user-fiendly of choices and for additional fields"""
        context = super().get_context_data(**kwargs)
        context ['blood_type'] = self.object.get_blood_type_display()
        context ['gender'] = self.object.get_gender_display()
        context ['total_cholesterol'] = self.object.total_cholesterol
        context ['heart_risk'] = self.object.heart_risk
        return context


class PatientCreateView(CreateView):
    model = Patient
    form_class = PatientForm

    def get_success_url(self):
        return reverse('detail_patient_view', kwargs={'pk': self.object.emp_number})
