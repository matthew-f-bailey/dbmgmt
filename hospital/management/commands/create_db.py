from datetime import datetime

from django.core.management.base import BaseCommand
from django.core.management import call_command
from faker import Faker

from hospital.models.places import Clinic
from hospital.models.people import Patient, Surgeon, Physician, get_chief_of_staff
from hospital.models.skill_types import Skills, SurgeryType
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

        # Create some surgeons
        surgeon1 = Surgeon(
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
        surgeon1.save()
        # Skills -> surgeon1.skills_set
        for skill in ["brain", "head_trauma"]:
            Skills(surgeon=surgeon1, skill=skill).save()
        print("Created Neurosurgeon")
