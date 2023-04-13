from datetime import datetime
import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from hospital.models.illnesses import Illness, Allergy, Medication
from hospital import constants


def get_chief_of_staff():
    """ Get the chief of staff, special physisican """
    cos = Physician.objects.get_or_create(
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
    return cos[0]


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

    def __str__(self) -> str:
        return f"{self.last_name}, {self.first_name}"

class SkilledPerson(Person):
    """ A person who can have skills assigned to them """
    ...

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
class Surgeon(SkilledPerson, Contract):
    specialty = models.CharField(max_length=254, choices=constants.SPECIALTIES)

    def can_perform(self, type):
        """
        type [SurgeryType]
        Given a SurgeryType, checks if this surgeon can perform the surgery
        NEEDS ALL SKILLS
        """
        skills = {s.skill.name for s in self.assignedskills_set.all()}
        needed = {s.name for s in type.requirements.all()}
        return needed.issubset(skills)

class Nurse(SkilledPerson, Salaried):
    """
    Cannot be assigned more than 1 surg type
    All types of surgeries have at least 2 nurses
    """
    grade = models.CharField(max_length=10, choices=constants.NURSE_GRADES)
    years_of_experience = models.PositiveIntegerField()

    def can_perform(self, type):
        """
        type [SurgeryType]
        Given a SurgeryType, checks if this nurse can assist
        NEEDS ANY 1 SKILL REQUIRED BY TYPE TO ASSIST
        """
        skills = {s.skill.name for s in self.assignedskills_set.all()}
        needed = {s.name for s in type.requirements.all()}
        for skill in skills:
            # If any 1 skill nurse has is found, they can perform
            if skill in needed:
                return True
        return False


class Physician(Person, Salaried):
    specialty = models.CharField(max_length=50, choices=constants.SPECIALTIES)

    @classmethod
    def get_chief_of_staff(cls):
        """ Since pk is emp_number, we need this to set default
        Default keyword wants pk, not instance

        Returns the PK of the Chief of staff
        """
        cos = get_chief_of_staff()
        return cos.emp_number

class Patient(Person):

    # Patients have 1 physician, if leaves, give to chief of staff
    pcp = models.ForeignKey(
        Physician,
        on_delete=models.SET(get_chief_of_staff),
        default=Physician.get_chief_of_staff,
        blank=True,
        null=True
    )
    illnesses = models.ManyToManyField(Illness)
    allergies = models.ManyToManyField(Allergy)

    # Medical Data
    blood_type = models.CharField(max_length=30, choices=constants.BLOOD_TYPE)
    blood_sugar = models.FloatField()
    cholesterol_hdl = models.FloatField()
    cholesterol_ldl = models.FloatField()
    cholesterol_tri = models.FloatField()


# in-paitent is a patient who needs a bed and nurse
class InPatient(Patient):
    # Room data
    admission_date = models.DateField(null=True)
    # We only need bed, as bed has a room, room has a unit
    bed = models.ForeignKey(
        "Bed",
        on_delete=models.CASCADE,
        null=True
    )
    assigned_nurse = models.ForeignKey(
        Nurse
    )

