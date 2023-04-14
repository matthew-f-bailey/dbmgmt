from django.db import models
from hospital.constants import MED_INTERACTION

# ================= #
# ==== ILLNESS ==== #
# ================= #
class Illness(models.Model):
    name = models.CharField(max_length=256)
    illness_code = models.CharField(max_length=10)
    description = models.CharField(max_length=1_000)


class Medication(models.Model):
    name = models.CharField(max_length=30)
    dosage = models.FloatField(max_length=30)
    frequency = models.CharField(max_length=100)

    # Lists of interactions this med may have
    interaction = models.ManyToManyField("self", through="Interactions")

# Interactions intermediate table
class Interactions(models.Model):
    med1 = models.ForeignKey(Medication, on_delete = models.CASCADE, related_name="first_med")
    med2 = models.ForeignKey(Medication, on_delete = models.CASCADE, related_name = "second_med")
    severity = models.CharField(choices=MED_INTERACTION, max_length=1)


class Allergy(models.Model):
    name = models.CharField(max_length=100)
    allergy_code = models.CharField(max_length=10)
    description = models.CharField(max_length=1_000)