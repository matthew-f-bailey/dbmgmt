""" Skills and types """
from django.db import models

from hospital import constants

class Skills(models.Model):
    """ A skill needed for a type of surgery """
    surgeon = models.ForeignKey(
        "Surgeon",
        on_delete=models.CASCADE, # Delete skill if surgeon gone
    )
    skill = models.CharField(
        choices=constants.SURGICAL_SKILLS,
        max_length=50
    )


class SurgeryType(models.Model):
    """
    A certain type of surgery
    Requires many skills to complete
    """
    requirements = models.ManyToManyField("Skills")
