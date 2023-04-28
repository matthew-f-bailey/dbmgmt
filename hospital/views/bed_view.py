from django.urls import reverse
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from hospital.forms.bed_form import BedForm
from hospital.models.places import Bed

class BedListView(ListView):
    """ Basic List View to show BedListView """

    # specify the model for list view
    model = Bed

    def get_queryset(self, *args, **kwargs):
        """ Do any orders, filters, etc """
        qs = super(BedListView, self).get_queryset(*args, **kwargs)
        # qs = qs.order_by("last_name")
        return qs

class BedDetailView(DetailView):
    model = Bed

class BedCreateView(CreateView):
    model = Bed
    form_class = BedForm

    def get_success_url(self):
        return reverse('detail_bed_view', kwargs={'pk': self.object.id})
