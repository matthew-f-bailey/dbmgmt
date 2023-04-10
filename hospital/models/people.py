from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
import uuid

from hospital.models.illnesses import Illness, Allergy, Medication
#from hospital.models.actions import Perscription
from hospital import constants


def get_chief_of_staff():
    """ Get the chief of staff, special physisican """
    return Physician.objects.get_or_create()


class Person(models.Model):
    """ Base model for all people """
    emp_number = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    dob = models.DateField()
    gender = models.CharField(max_length=2, choices= constants.GENDER)
    address = models.CharField(max_length=254)
    phone = models.CharField(max_length=30)
    SSN = models.PositiveIntegerField()

class Salaried(models.Model):
    """ Salaried Emps """
    salary = models.PositiveIntegerField(
        validators=[MinValueValidator(25_000), MaxValueValidator(300_000)]
    )


class Contract(models.Model):
    """ Contract Emps """
    length = models.PositiveIntegerField()
    type = models.CharField(max_length=30)

# ================ #
# ==== PEOPLE ==== #
# ================ #
class Surgeon(Person, Contract):
    specialty = models.CharField(max_length=254, choices=constants.SPECIALTIES)


class Nurse(Person, Salaried):
    grade = models.CharField(max_length=254, choices=constants.NURSE_GRADES)
    years_of_experience = models.PositiveIntegerField()


class Physician(Person, Salaried):
    specialty = models.CharField(max_length=254, choices=constants.SPECIALTIES)



class Patient(Person):

    # Patients have 1 physician, if leaves, give to chief of staff
    primary_physician = models.ForeignKey(
        Physician,
        on_delete=models.SET(get_chief_of_staff),
        blank=True, null=True
    )
    illnesses = models.ManyToManyField(Illness, blank=True, null=True)
    allergies = models.ManyToManyField(Allergy, blank=True, null=True)

    # Deleting a perscription, deletes rel/ 
    # a patient may have multiple medications. We need to have a seperate table for prescribtions
    #perscriptions = models.ForeignKey(
    #   Perscription,
    #   on_delete=models.CASCADE
    #)

    # Medical Data
    blood_type = models.CharField(max_length=30, choices=constants.BLOOD_TYPE)
    blood_sugar = models.FloatField()
    cholesterol_hdl = models.FloatField()
    cholesterol_ldl = models.FloatField()
    cholesterol_tri = models.FloatField()
