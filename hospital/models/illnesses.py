from django.db import models

# ================= #
# ==== ILLNESS ==== #
# ================= #
class Illness(models.Model):
    pass


class Medication(models.Model):
    name = models.CharField(max_length=30)
    dosage = models.FloatField(max_length=30)

    # Lists of interactions this med may have
    interactions_severe = models.ManyToManyField("self")
    interactions_moderate = models.ManyToManyField("self")
    interactions_little = models.ManyToManyField("self")


class Allergy(models.Model):
    pass