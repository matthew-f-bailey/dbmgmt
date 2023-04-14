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
    patient = models.ForeignKey(
        "Patient",
        on_delete=models.CASCADE
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



class Consultation(models.Model):
    """ The act of a patient seeing a physician
    Serves as scheudle of visits
    """
    physician = models.ForeignKey(
        "Physician",
        on_delete=models.CASCADE
    )
    patient = models.ForeignKey(
        "Patient",
        on_delete=models.CASCADE
    )
    date = models.DateField()

    def __str__(self) -> str:
        return (
            f"Patient '{self.patient}' seeing Physician "
            f"'{self.physician}' ({self.physician.specialty}) @ {self.date}"
        )


class Prescriptions(models.Model):
    """ Ties which dr gave which patient some med """
    physician = models.ForeignKey(
        "Physician",
        on_delete=models.SET_NULL,
        null=True
    )
    # If patient or med deletes, remove this prescription
    patient = models.ForeignKey(
        "Patient",
        on_delete=models.CASCADE
    )
    medication = models.ForeignKey(
        "Medication",
        on_delete=models.CASCADE
    )
    frequency = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)