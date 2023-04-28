from django.urls import path
from hospital.views import home_view
from hospital.views import people_view
from hospital.views import medication_view
from hospital.views import consutation_view
from hospital.views import surgery_view
from hospital.views import perscription_view


urlpatterns = [
    path('', home_view.home_view , name='hospital-home'),
    # Patient Create/List/Detail
    path('create_patient', people_view.PatientCreateView.as_view(template_name="create_form.html") , name='create_patient_view'),
    path('list_patient.html', people_view.PatientListView.as_view(template_name="patient_list.html") , name='list_patient_view'),
    path('detail_patient/<pk>', people_view.PatientDetailView.as_view(template_name="patient_detail.html") , name='detail_patient_view'),
    # Medication
    path('create_medication.html', medication_view.MedicationCreateView.as_view(template_name="create_form.html"), name='create_medication_view'),
    path('medication_interaction.html', medication_view.CreateMedicationInteraction.as_view(template_name="create_form.html"), name='create_medication_interaction'),
    path('view_medications.html/<int:pk>/', medication_view.MedicationDetailView.as_view(), name='view_medications'),
    path('view_medications.html', medication_view.MedicationListView.as_view(), name='view_medications'),
    # Consultations
    path('create_consultation', consutation_view.ConsultationCreateView.as_view(template_name="create_form.html"), name='create_consultation_view'),
    path('view_consultation/<int:pk>/', consutation_view.ConsultationDetailView.as_view(template_name="consultation_detail.html"), name='detail_consultation_view'),
    path('list_consultation', consutation_view.ConsultationListView.as_view(template_name="consultation_list.html"), name='list_consultation_view'),
    # Surgeries
    path('create_surgery', surgery_view.SurgeryCreateView.as_view(template_name="create_form.html"), name='create_surgery_view'),
    path('view_surgery/<int:pk>/', surgery_view.SurgeryDetailView.as_view(template_name="surgery_detail.html"), name='detail_surgery_view'),
    path('list_surgery', surgery_view.SurgeryListView.as_view(template_name="surgery_list.html"), name='list_surgery_view'),
    # Perscriptions
    path('create_perscription', perscription_view.PerscriptionCreateView.as_view(template_name="create_form.html"), name='create_perscription_view'),
    path('view_perscription/<int:pk>/', perscription_view.PerscriptionDetailView.as_view(template_name="perscription_detail.html"), name='detail_perscription_view'),
    path('list_perscription', perscription_view.PerscriptionListView.as_view(template_name="perscription_list.html"), name='list_perscription_view'),
]
