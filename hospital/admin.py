from django.contrib import admin

from .models.places import *

# adding Clinic, Unit, Room tables to admin page
adminpage = {Clinic, Unit, Room }
admin.site.register(adminpage)