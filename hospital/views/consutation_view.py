from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from hospital.forms.consultation_form import ConsultationForm
from hospital.models.actions import Consultation

class ConsultationListView(ListView):
    """ Basic List View to show consultations """

    # specify the model for list view
    model = Consultation

    def get_queryset(self, *args, **kwargs):
        """ Do any orders, filters, etc """
        qs = super(ConsultationListView, self).get_queryset(*args, **kwargs)
        # qs = qs.order_by("last_name")
        return qs

class ConsultationDetailView(DetailView):
    model = Consultation

class ConsultationCreateView(CreateView):
    model = Consultation
    form_class = ConsultationForm

    def get_success_url(self):
        return reverse('detail_consultation_view', kwargs={'pk': self.object.id})
