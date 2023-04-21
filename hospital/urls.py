from django.urls import path
from hospital.views import home_view
from hospital.views import people_view
from hospital.views import medication_view


urlpatterns = [
    path('', home_view.home_view , name='hospital-home'),
    path('create_patient.html', people_view.create_patient_view , name='create_patient_view'),
    path('create_medication.html', medication_view.create_medication_view , name = 'create_medication_view'),
    path('medication_interaction.html', medication_view.create_medication_interaction , name = 'create_medication_interaction'),
    path('view_medications.html/<int:pk>/', medication_view.MedicationDetailView.as_view(), name = 'view_medications'),
    path('view_medications.html', medication_view.MedicationListView.as_view(), name = 'view_medications')
]
