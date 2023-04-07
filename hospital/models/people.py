from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
import uuid

from hospital.models.illnesses import Illness, Allergy, Medication
from hospital.models.actions import Perscription
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
    gender = models.Choices(choices=constants.GENDER)
    address = models.CharField()
    phone = models.CharField()


class Salaried(models.Model):
    """ Salaried Emps """
    salary = models.PositiveIntegerField(
        validators=[MinValueValidator(25_000), MaxValueValidator(300_000)]
    )


class Contract(models.Model):
    """ Contract Emps """
    length = models.PositiveIntegerField()
    type = models.CharField()

# ================ #
# ==== PEOPLE ==== #
# ================ #
class Surgeon(Person, Contract):
    pass


class Nurse(Person, Salaried):
    grade = models.Choices(choices=constants.NURSE_GRADES)
    years_of_experience = models.PositiveIntegerField()


class Physician(Person, Salaried):
    specialty = models.Choices(choices=constants.SPECIALTIES)



class Patient(Person):

    # Patients have 1 physician, if leaves, give to chief of staff
    physician = models.ForeignKey(
        Physician,
        on_delete=models.SET(get_chief_of_staff)
    )
    illnesses = models.ManyToManyField(Illness)
    allergies = models.ManyToManyField(Allergy)

    # Deleting a perscription, deletes rel
    perscriptions = models.ForeignKey(
        Perscription,
        on_delete=models.CASCADE
    )

    # Medical Data
    blood_type = models.Choices(choices=constants.BLOOD_TYPE)
    blood_sugar = models.FloatField()
    cholesterol_hdl = models.FloatField()
    cholesterol_ldl = models.FloatField()
    cholesterol_tri = models.FloatField()
