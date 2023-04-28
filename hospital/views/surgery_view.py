from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from hospital.forms.surgery_form import SurgeryForm
from hospital.models.actions import Surgery


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

    def get_success_url(self):
        return reverse('detail_surgery_view', kwargs={'pk': self.object.id})
