from datetime import datetime
import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from hospital.models.illnesses import Illness, Allergy, Medication
from hospital import constants


def get_chief_of_staff():
    """ Get the chief of staff, special physisican """
    cof = Physician.objects.get_or_create(
        first_name="Chief",
        last_name="Staffton",
        dob=datetime(1960, 1, 1),
        gender="M",
        address="10 Chiefton Way",
        phone="5557891234",
        specialty=constants.SPECIALTIES[0][0],
        salary=300_000,
        ssn="123-45-6789"
    )
    # Returns bool of "if created" in cof[1]
    return cof[0]


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
    ssn = models.CharField(max_length=11)

class Salaried(models.Model):
    """ Salaried Emps """
    salary = models.PositiveIntegerField(
        validators=[MinValueValidator(25_000), MaxValueValidator(300_000)]
    )


class Contract(models.Model):
    """ Contract Emps """
    contract_length = models.PositiveIntegerField()
    contract_type = models.CharField(max_length=50)

# ================ #
# ==== PEOPLE ==== #
# ================ #
class Surgeon(Person, Contract):
    specialty = models.CharField(max_length=254, choices=constants.SPECIALTIES)


class Nurse(Person, Salaried):
    """
    Cannot be assigned more than 1 surg type
    All types of surgeries have at least 2 nurses
    """
    surgery_type = models.CharField(max_length=50, choices=constants.SPECIALTIES)
    grade = models.CharField(max_length=10, choices=constants.NURSE_GRADES)
    years_of_experience = models.PositiveIntegerField()


class Physician(Person, Salaried):
    specialty = models.CharField(max_length=50, choices=constants.SPECIALTIES)



class Patient(Person):

    # Patients have 1 physician, if leaves, give to chief of staff
    pcp = models.ForeignKey(
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
