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


class PatientCreateView(CreateView):
    model = Patient
    form_class = PatientForm

    def get_success_url(self):
        return reverse('detail_patient_view', kwargs={'pk': self.object.emp_number})
