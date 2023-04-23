from django.shortcuts import render
from django.urls import reverse
from hospital.forms.medication_form import MedicationForm, InteractionForm
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from hospital.models.illnesses import Medication, Interactions

# To add a new medication
class MedicationCreateView(CreateView):
    model = Medication
    form_class = MedicationForm

    def get_success_url(self):
        return reverse('view_medications', kwargs={'pk': self.object.id})


# class based view to view medications
class MedicationListView(ListView):
    model = Medication
    template_name = 'medication_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # count interactions and add them to context
        for object in context['object_list']:
            interactions_count = (
                Interactions.objects.filter(medication1=object.id ).count() +
                Interactions.objects.filter(medication2=object.id ).count() 
                )
            object.interactions_count = interactions_count
        return context


# detail view for each medication to show medication details and medicaiton interactions
class MedicationDetailView(DetailView):
    model = Medication
    template_name = 'Medication_detail_view.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)

        # get list of interactions while shown medication is in medication1 of th table
        interacts_left = Interactions.objects.filter(medication1_id = self.kwargs['pk'])

        # get list of interactions while shown medication is in medication2 of th table
        interacts_right = Interactions.objects.filter(medication2_id = self.kwargs['pk'])

        # append interacting medications data
        interacts_with = []
        for interaction in interacts_left:
            interacts_with.append([interaction.medication2.id, interaction.medication2.code, 
                                   interaction.medication2.name , interaction.get_severity_display()])
        for interaction in interacts_right:
            interacts_with.append([interaction.medication1.id, interaction.medication1.code, 
                                   interaction.medication1.name , interaction.get_severity_display()])
        
        context ['interactions'] = interacts_with
        return context
    


# To add interaction between medications

class CreateMedicationInteraction(CreateView):
    model = Interactions
    form_class = InteractionForm

    def form_valid(self, form):
        if ( form.cleaned_data['medication1'] == form.cleaned_data['medication2'] ):
            form.add_error('medication2' ,"Can't add interaction to the same medication")
            return super().form_invalid(form)
        elif(Interactions.objects.filter(medication1 = form.cleaned_data['medication1'], 
                                         medication2 = form.cleaned_data['medication2']).exists() or
             Interactions.objects.filter(medication1 = form.cleaned_data['medication2'], 
                                         medication2 = form.cleaned_data['medication1']).exists()
                                           ):
            messages.error(self.request, "Interactin already exists")
            return super().form_invalid(form)
            
        messages.success(self.request, "Interaction has been saved")
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('create_medication_interaction')

