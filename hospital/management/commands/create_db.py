from datetime import datetime

from django.core.management.base import BaseCommand
from django.core.management import call_command
from faker import Faker

from hospital.models.places import Clinic
from hospital.models.people import (
    Nurse,
    Patient,
    Physician,
    Surgeon,
    get_chief_of_staff,
)
from hospital.models.skill_types import Skills, SurgeonSkills, SurgeryType
from hospital import constants


fake = Faker()

class Command(BaseCommand):
    help = 'Deletes current and recreates the mock database'

    def handle(self, *args, **options):
        """ Call the command """

        # Verify migrations are made and db gets them
        call_command("flush")
        call_command("makemigrations")
        call_command("migrate")

        # Start creating mock data and relations
        print("Mocking up the database...")

        # Create our Chief of Staff (Also a Physician)
        chief = get_chief_of_staff()
        print(f"Created our Chief of Staff '{chief.first_name} {chief.last_name}'")

        # Creating entire skills table
        for skill, readable in constants.SURGICAL_SKILLS:
            Skills(name=skill).save()

        # Create some surgeons
        neurosurgeon = Surgeon(
            first_name="Joan",
            last_name="Neuro",
            dob=datetime(1970, 2, 2),
            gender="F",
            address="10 Brain Lane",
            phone="1298763490",
            contract_length=5,
            contract_type="Per Surgery",
            ssn=fake.ssn()
        )
        neurosurgeon.save()

        # Create a Neruosurgery type and give surgeon exact skills needed
        neuro_skills = ["brain", "head_trauma"]
        neurosurgury = SurgeryType(name="Neurosurgery")
        neurosurgury.save()
        for skill in neuro_skills:
            # User will be presented these in view
            skill_instance = Skills.objects.get(name=skill)

            # Add skill to surgeon
            SurgeonSkills(surgeon=neurosurgeon, skill=skill_instance).save()

            # Add to this skill type of neurosurgery
            neurosurgury.requirements.add(skill_instance)
            neurosurgury.save()

        # Should be good here
        if neurosurgeon.can_perform(neurosurgury):
            print("Created Neurosurgeon that can perform Neurosurgery")
        else:
            raise RuntimeError("Hmm.. Check into can_perform method..")
