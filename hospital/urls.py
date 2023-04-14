from django.urls import path
from hospital.views import home_view
from hospital.views import people_view


urlpatterns = [
    path('', home_view.home_view , name='hospital-home'),
    path('create_patient.html', people_view.create_patient_view , name='create_patient_view')
]
