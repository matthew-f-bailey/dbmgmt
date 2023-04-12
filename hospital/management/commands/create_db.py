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
from hospital.models.skill_types import Skills, AssignedSkills, SurgeryType
from hospital import constants


fake = Faker()

class Command(BaseCommand):
    help = 'Deletes current and recreates the mock database'

    def populate_constants(self):
        """ Populate constants into their own tables """

        # Creating entire skills table
        for skill, _ in constants._SURGICAL_SKILLS:
            s = Skills(name=skill)
            s.save()
            print("Created skill of", s)

        # Surgery types made of skills
        def create_type(name, skills: list):
            stype = SurgeryType(name=name)
            stype.save()
            for skill in skills:
                stype.requirements.add(Skills.objects.get(name=skill))
                stype.save()
            print(f"Created SurgeryType of {stype}")

        create_type("general_surgery", ["transplant", "wound"])
        create_type("neurosurgery", ["brain", "head_trauma"])
        create_type("cardiac_surgery", ["cardiac_arrest", "heart_valve"])
        create_type("plastic_surgery", ["rhinoplasty", "facelift"])

    def create_neurosurgeon(self):
        """ Creates a neurosurgeon and makes sure he can perform """
        # Create neuro
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

        # Give neurosurgeon the right skills
        neuro_skills = ["brain", "head_trauma"]
        for skill in neuro_skills:
            # User will be presented these in view
            skill_instance = Skills.objects.get(name=skill)

            # Add skill to surgeon
            AssignedSkills(person=neurosurgeon, skill=skill_instance).save()

        # Should be good here
        neurosurgury = SurgeryType.objects.get(name="neurosurgery")
        if neurosurgeon.can_perform(neurosurgury):
            print("Created Neurosurgeon that can perform Neurosurgery")
        else:
            raise RuntimeError("Hmm.. Check into can_perform method..")

        return neurosurgeon

    def create_plastic_surgeon(self):
        """ Creates a plastic and makes sure he can perform """
        # Create surgeon
        plastic_surgeon = Surgeon(
            first_name="Ken",
            last_name="Plasty",
            dob=datetime(1965, 3, 3),
            gender="M",
            address="10 Botox Ave",
            phone="8760981234",
            contract_length=3,
            contract_type="Per Surgery",
            ssn=fake.ssn()
        )
        plastic_surgeon.save()

        # Give neurosurgeon the right skills
        plastic_skills = ["rhinoplasty", "facelift"]
        for skill in plastic_skills:
            # User will be presented these in view
            skill_instance = Skills.objects.get(name=skill)

            # Add skill to surgeon
            AssignedSkills(person=plastic_surgeon, skill=skill_instance).save()

        # Double check he can do whats expected
        plastic = SurgeryType.objects.get(name="plastic_surgery")
        neuro = SurgeryType.objects.get(name="neurosurgery")
        if plastic_surgeon.can_perform(plastic):
            print("Created Plastic Surgeon that can perform Plastic Surgery")
        else:
            raise RuntimeError("Hmm.. Check into can_perform method..")

        # Verify he can't do neuro
        if plastic_surgeon.can_perform(neuro):
            raise("Nope, plastic surgeon shouldn't be able to do Neurosurgery")

        return plastic_surgeon

    def create_plastic_nurse(self):
        """ Creates a plastic nurse"""
        # Create surgeon
        nurse = Nurse(
            first_name="Ken",
            last_name="Plasty",
            dob=datetime(1965, 3, 3),
            gender="M",
            address="10 Botox Ave",
            phone="8760981234",
            salary=120_000,
            ssn=fake.ssn(),
            grade="a",
            years_of_experience=5,
        )
        nurse.save()

        # Give nurse plastic surgery skill
        skill_instance = Skills.objects.get(name="facelift")

        # Add skill to Nurse
        AssignedSkills(person=nurse, skill=skill_instance).save()

        # Double check he can do whats expected
        plastic = SurgeryType.objects.get(name="plastic_surgery")
        neuro = SurgeryType.objects.get(name="neurosurgery")
        if nurse.can_perform(plastic):
            print("Created Plastic Surgery Nurse to assist")
        else:
            raise RuntimeError("Hmm.. Check into can_perform method..")

        # Verify he can't do neuro
        if nurse.can_perform(neuro):
            raise("Nope, plastic Nurse shouldn't be able assist in Neurosurgery")

        return nurse

    def handle(self, *args, **options):
        """ Call the command """

        # Verify migrations are made and db gets them
        call_command("flush")
        call_command("makemigrations")
        call_command("migrate")

        # Start creating mock data and relations
        print("Mocking up the database...")

        # Create skills, types, etc
        self.populate_constants()

        # Create our Chief of Staff (Also a Physician)
        chief = get_chief_of_staff()
        print(f"Created our Chief of Staff '{chief.first_name} {chief.last_name}'")

        # Create a neurosurgeon
        neurosurgeon = self.create_neurosurgeon()

        # Create plastic surgeon
        plastic_surgeon = self.create_plastic_surgeon()

        # Create a plastic surgery nurse
        plastic_nurse = self.create_plastic_nurse()