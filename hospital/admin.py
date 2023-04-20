from django.contrib import admin

from .models.places import *
from .models.people import Patient, InPatient
from .models.illnesses import Medication, Interactions

# adding Clinic, Unit, Room tables to admin page
adminpage = {Clinic, Unit, Room, Patient, Medication, Interactions }
admin.site.register(adminpage)