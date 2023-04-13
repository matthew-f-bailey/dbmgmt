""" Skills and types
- Surgeons have skills
- A Surgery has a SurgeryType made of skills
- If a surgeon has all those skills, he can perform it
"""
from django.db import models

from hospital import constants

class Skills(models.Model):
    """ The db containing all skills people can have
    New skills can be added but to avoid hard coding in constants
    """
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class SurgeryType(models.Model):
    """
    Defines a type of surgery and what skills are needed by the surgeon to complete it
    Nurses will also have one of these types assigned to them but don't need to worry
    about specific skills
    """
    name = models.CharField(max_length=50)
    requirements = models.ManyToManyField("Skills")

    def __str__(self) -> str:
        reqs = [r.name for r in self.requirements.all()]
        return f"{self.name} - {reqs}"


class AssignedSkills(models.Model):
    """ Links up what surgeons have what skills """
    # All skilled persons can have skills
    # nurses, surgeons need skills to perform surgeries
    person = models.ForeignKey(
        "SkilledPerson",
        on_delete=models.CASCADE, # Delete skill link if person gone
    )
    skill = models.ForeignKey(
        "Skills",
        on_delete=models.CASCADE # Delete this entry if skill removed
    )

    def __str__(self) -> str:
        return f"{self.person.last_name}, {self.person.first_name} - {self.skill.name}"
