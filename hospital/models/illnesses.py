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
    code = models.PositiveIntegerField()
    available_qnty = models.PositiveIntegerField()
    cost = models.FloatField()
    usage = models.CharField(max_length=254)

    # Lists of interactions this med may have
    interaction = models.ManyToManyField("self", through="Interactions", symmetrical=False)
    def __str__(self) -> str:
        return f"{self.code}, {self.name}"

# Interactions intermediate table
class Interactions(models.Model):
    medication1 = models.ForeignKey(Medication, on_delete = models.CASCADE, related_name = "first_med")
    medication2 = models.ForeignKey(Medication, on_delete = models.CASCADE, related_name = "second_med")
    severity = models.CharField(choices=MED_INTERACTION, max_length=1)
    # to avoid duplicate records of interaction between the same medciations
    class Meta:
        unique_together = ('medication1','medication2')

    def __str__(self) -> str:
        return f"{self.medication1} x {self.medication2} ({self.severity})"

class Allergy(models.Model):
    name = models.CharField(max_length=100)
    allergy_code = models.CharField(max_length=10)
    description = models.CharField(max_length=1_000)

    def __str__(self):
        return self.name
