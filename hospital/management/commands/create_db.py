import os
import shutil
from datetime import datetime

from django.core.management.base import BaseCommand
from django.core.management import call_command
from faker import Faker

from hospital.models.actions import Consultation
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

from dbmgmt.settings import BASE_DIR

fake = Faker()

class Command(BaseCommand):
    help = 'Deletes current and recreates the mock database'

    def reset_db(self):
        # Verify migrations are made and db gets them
        try:
            os.remove(f"{BASE_DIR}/db.sqlite3")
        except FileNotFoundError:
            pass
        shutil.rmtree(f"{BASE_DIR}/hospital/migrations", ignore_errors=True)
        call_command("makemigrations", "hospital")
        call_command("makemigrations")
        call_command("migrate", "hospital")
        call_command("migrate")

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

    def create_general_physician(self):
        phys = Physician(
            specialty="general",
            salary=150_000,
            first_name="Al",
            last_name="Gener",
            dob=datetime(1940, 5, 5),
            gender="M",
            address="123 General Way",
            phone=fake.phone_number(),
            ssn=fake.ssn(),
        )
        phys.save()
        print(f"Created Physician of '{phys}'")
        return phys

    def create_optomotrist(self):
        phys = Physician(
            specialty="optometry",
            salary=180_000,
            first_name="Cornealeus",
            last_name="John",
            dob=datetime(1945, 5, 5),
            gender="M",
            address="123 Eye Ct",
            phone=fake.phone_number(),
            ssn=fake.ssn(),
        )
        phys.save()
        print(f"Created Optomotrist of '{phys}'")
        return phys

    def create_general_patient(self):
        patient = Patient(
            first_name="Pat",
            last_name="Entman",
            dob=datetime(1980, 5, 5),
            gender="M",
            address="123 Patient Dr",
            phone=fake.phone_number(),
            ssn=fake.ssn(),
            blood_type="op",
            blood_sugar="12",
            cholesterol_hdl="6",
            cholesterol_ldl="5",
            cholesterol_tri="8",
        )
        patient.save()
        print(f"Created Patient of '{patient}'")
        return patient


    def handle(self, *args, **options):
        """ Call the command """

        self.reset_db()

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

        # Create a physicians
        general_physician = self.create_general_physician()
        optomotrist = self.create_optomotrist()

        # Create a patient (auto assigned to cheif)
        general_patient = self.create_general_patient()
        assert general_patient.pcp == chief

        # Assign patient from COF to general
        general_patient.pcp = general_physician
        general_patient.save()

        # Get this patient in for consultation
        general_patient_visit = Consultation(
            physician=general_physician,
            patient=general_patient,
            date=datetime.now()
        )
        general_patient_visit.save()
        print(general_patient_visit)

        # Patient can also see opt, who is not primary
        opt_visit = Consultation(
            physician=optomotrist,
            patient=general_patient,
            date=datetime(2023, 8, 1)
        )
        print(opt_visit)
