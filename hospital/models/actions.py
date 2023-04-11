from django.db import models

from hospital import constants


class Surgery(models.Model):
    """
    The act of a surgery, works as schedule
    """
    date = models.CharField(max_length=30)
    surgeon = models.ForeignKey(
        "Surgeon",
        null=True,
        on_delete=models.SET_NULL
    )
    nurse = models.ForeignKey(
        "Nurse",
        null=True,
        on_delete=models.SET_NULL
    )
    code = models.CharField(
        choices=constants.SURGERY_CODES,
        max_length=5
    )
    anatomical_location = models.CharField(
        max_length=100,
        choices=constants.ANATOMICAL_LOCATIONS
    )
    category = models.CharField(
        max_length=100,
        choices=constants.SURGERY_CATEGORIES
    )
    type = models.ForeignKey(
        "SurgeryType",
        on_delete=models.SET_NULL,
        null=True
    )
    special_needs = models.CharField(max_length=100)



class Appointments(models.Model):
    """ The act of a patient seeing a physician """
    ...


class Perscriptions(models.Model):
    """ Ties which dr gave which patient some med """
    ...