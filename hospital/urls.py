from django.urls import path
from hospital.views import home_view
from hospital.views import people_view
from hospital.views import medication_view


urlpatterns = [
    path('', home_view.home_view , name='hospital-home'),
    # Patient Create/List/Detail
    path('create_patient', people_view.PatientCreateView.as_view(template_name="create_form.html") , name='create_patient_view'),
    path('list_patient.html', people_view.PatientListView.as_view(template_name="patient_list.html") , name='list_patient_view'),
    path('detail_patient/<pk>', people_view.PatientDetailView.as_view(template_name="patient_detail.html") , name='detail_patient_view'),
    # Medication
    path('create_medication.html', medication_view.MedicationCreateView.as_view(template_name="create_form.html") , name = 'create_medication_view'),
    path('medication_interaction.html', medication_view.CreateMedicationInteraction.as_view(template_name="create_form.html") , name = 'create_medication_interaction'),
    path('view_medications.html/<int:pk>/', medication_view.MedicationDetailView.as_view(), name = 'view_medications'),
    path('view_medications.html', medication_view.MedicationListView.as_view(), name = 'view_medications')
]
