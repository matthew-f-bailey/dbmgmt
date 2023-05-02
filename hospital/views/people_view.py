from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from hospital.forms.people_form import PatientForm, StaffToPatient
from hospital.models.people import Patient, Physician, Person, Surgeon, Nurse
from hospital.models.actions import Perscriptions, Surgery


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
    

class ManagePhysicians(ListView):
    """ List view to manage physicians """

    # specify the model for list view
    model = Physician

    # order by last name
    def get_queryset(self, *args, **kwargs):
        """ Do any orders, filters, etc """
        qs = super(ManagePhysicians, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("last_name")
        return qs
    
    # get count of patients and count of presciptions
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for physician in context['object_list']:
            physician.patients = Patient.objects.filter(pcp = physician.person_ptr_id).count()
            physician.perscriptions = Perscriptions.objects.filter(physician_id = physician.person_ptr_id).count()
            # check if has a record in patient table
            if (Patient.objects.filter(person_ptr = physician.person_ptr).exists()):  
                physician.isPatient = True
        return context
    
class ManageSurgeons(ListView):
    """ List view to manage surgeons """

    # specify the model for list view
    model = Surgeon

    # order by last name
    def get_queryset(self, *args, **kwargs):
        """ Do any orders, filters, etc """
        qs = super(ManageSurgeons, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("last_name")
        return qs
    
    # get count of scheduled surgeries
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for surgeon in context['object_list']:
            surgeon.surgeries = Surgery.objects.filter(surgeon = surgeon.person_ptr_id).count()
            # check if has a record in patient table
            if (Patient.objects.filter(person_ptr = surgeon.person_ptr).exists()):  
                surgeon.isPatient = True
        return context
    
class ManageNurses(ListView):
    """ List view to manage nurses """

    # specify the model for list view
    model = Nurse

    # order by last name
    def get_queryset(self, *args, **kwargs):
        """ Do any orders, filters, etc """
        qs = super(ManageNurses, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("last_name")
        return qs
    
    # get count of assigned patients
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for nurse in context['object_list']:
            nurse.patients = Patient.objects.filter(assigned_nurse = nurse).count()
            nurse.surgeries = Surgery.objects.filter(nurse = nurse).count()
            # check if has a record in patient table
            if (Patient.objects.filter(person_ptr = nurse.person_ptr).exists()):  
                nurse.isPatient = True
        return context
    
    

class AddStaffToPatient(CreateView):
    """ Add a staff members to patient table"""
    model = Patient
    form_class = StaffToPatient
    template_name  = 'staff_to_patient.html'
    
    # inherit instance from person to patient
    def form_valid(self, form: BaseModelForm) :
        person = Person.objects.get(pk = self.kwargs.get('pk') )
        form.instance.person_ptr = person
        form.instance.save_base(raw=True)
        form.instance.__dict__.update(person.__dict__)
        return super().form_valid(form)
    
    # add employee name to header
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['header'] = f""" Add medical data for employee { Person.objects.get(pk = self.kwargs.get('pk') ).last_name},
                                {Person.objects.get(pk = self.kwargs.get('pk') ).first_name}
                                 """
        return context

    def get_success_url(self):
        return reverse('detail_patient_view', kwargs={'pk': self.object.emp_number})