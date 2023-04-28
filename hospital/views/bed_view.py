from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from hospital.forms.bed_form import BedForm
from hospital.models.places import Bed, Unit
from hospital.models.people import Patient, Nurse

class UnitListView(ListView):
    """ Basic List View to show BedListView """

    # specify the model for list view
    model = Unit

    def get_queryset(self, *args, **kwargs):
        """ Do any orders, filters, etc """
        qs = super(UnitListView, self).get_queryset(*args, **kwargs)
        # qs = qs.order_by("last_name")
        return qs


class BedListView(ListView):
    """ Basic List View to show BedListView """

    # specify the model for list view
    model = Bed

    def get_queryset(self, *args, **kwargs):
        """ Do any orders, filters, etc """
        qs = super(BedListView, self).get_queryset(*args, **kwargs)
        # qs = qs.order_by("last_name")
        return qs


def assign_bed(request, pk):
    if request.method=="GET":
        bed = Bed.objects.get(id=pk)
        # Get eligable patients
        return render(
            request,
            "bed_detail.html",
            {
                "bed": bed,
                "patients": Patient.objects.all(),
                "nurses": Nurse.objects.all()
            }
        )

    else:
        # Get ids from post
        patient_id = request.POST.get("patient_id")
        bed_id = request.POST.get("bed_id")
        nurse_id = request.POST.get("nurse_id")
        # Get objects from ids
        patient = Patient.objects.get(emp_number=patient_id)
        nurse = Nurse.objects.get(emp_number=nurse_id)
        bed = Bed.objects.get(id=bed_id)

        # Assign to patient
        patient.bed = bed
        patient.assigned_nurse = nurse
        patient.save()

        return redirect(reverse("list_bed_room_unit_view"))

class BedDetailView(DetailView):
    model = Bed
