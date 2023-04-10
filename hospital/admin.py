from django.contrib import admin

from .models.places import *
from .models.people import Patient

# adding Clinic, Unit, Room tables to admin page
adminpage = {Clinic, Unit, Room, Patient }
admin.site.register(adminpage)