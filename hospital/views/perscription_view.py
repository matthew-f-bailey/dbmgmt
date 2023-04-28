from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from hospital.forms.perscription_form import PerscriptionForm
from hospital.models.actions import Perscriptions


class PerscriptionListView(ListView):
    """ Basic List View to show Perscription """

    # specify the model for list view
    model = Perscriptions

    def get_queryset(self, *args, **kwargs):
        """ Do any orders, filters, etc """
        qs = super(PerscriptionListView, self).get_queryset(*args, **kwargs)
        # qs = qs.order_by("last_name")
        return qs

class PerscriptionDetailView(DetailView):
    model = Perscriptions

class PerscriptionCreateView(CreateView):
    model = Perscriptions
    form_class = PerscriptionForm

    def get_success_url(self):
        return reverse('detail_perscription_view', kwargs={'pk': self.object.id})
