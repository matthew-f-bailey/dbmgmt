from django.db import models

from hospital.models.people import Surgeon, Nurse
from hospital import constants


class Surgery(models.Model):
    """
    The act of a surgery
    """
    date = models.CharField(max_length=30)
    surgeon = models.ForeignKey(
        Surgeon,
        on_delete=models.SET_NULL
    )
    nurse = models.ForeignKey(
        Nurse,
        on_delete=models.SET_NULL
    )
    code = models.Choices(choices=constants.SURGERY_CODES)
    anatomical_location = models.Choices(choices=constants.ANATOMICAL_LOCATIONS)
    category = models.Choices(choices=constants.SURGERY_CATEGORIES)
    special_needs = models.CharField()



class Appointment(models.Model):
    """ The act of a patient seeing a physician """
    ...


class Perscription(models.Model):
    """ Ties which dr gave which patient some med """
    ...