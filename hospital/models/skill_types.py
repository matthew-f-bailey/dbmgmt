""" Skills and types """
from django.db import models

from hospital import constants

class Skills(models.Model):
    """ The db containing all skills surgeons can have """
    name = models.CharField(max_length=100, choices=constants.SURGICAL_SKILLS)

    def __str__(self) -> str:
        return self.name


class SurgeryType(models.Model):
    """
    Defines a type of surgery and what skills are needed by the surgeon to complete it
    Nurses will also have one of these types assigned to them but don't need to worry
    about specific skills
    """
    name = models.CharField(max_length=50, primary_key=True)
    requirements = models.ManyToManyField("Skills")

    def __str__(self) -> str:
        reqs = [r.name for r in self.requirements.all()]
        return f"{self.name} - {reqs}"


class SurgeonSkills(models.Model):
    """ Links up what surgeons have what skills """
    surgeon = models.ForeignKey(
        "Surgeon",
        on_delete=models.CASCADE, # Delete skill if surgeon gone
    )
    skill = models.ForeignKey(
        "Skills",
        on_delete=models.CASCADE # Delete this entry if skill removed
    )

    def __str__(self) -> str:
        return f"{self.surgeon.last_name}, {self.surgeon.first_name} - {self.skill.name}"
