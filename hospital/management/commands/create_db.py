import os
import shutil
import random
from datetime import datetime

from django.core.management.base import BaseCommand
from django.core.management import call_command
from faker import Faker
from faker_biology.physiology import Organ
from faker_biology.taxonomy import ModelOrganism
from faker_biology.mol_biol import Enzyme
from faker_biology.bioseq import Bioseq

from hospital.models.actions import Consultation, Perscriptions, Surgery
from hospital.models.places import Unit, Bed, Room
from hospital.models.people import (
    Nurse,
    Patient,
    Physician,
    Surgeon,
    get_chief_of_staff,
)
from hospital.models.illnesses import Medication, Illness, Allergy
from hospital.models.skill_types import Skills, AssignedSkills, SurgeryType
from hospital import constants

from dbmgmt.settings import BASE_DIR

fake = Faker()
# Add some extra faker for illnesses and medicine
fake.add_provider(Organ) # Allows fake.organ()
fake.add_provider(ModelOrganism) # fake.organism_latin()  sounds like illness enough
fake.add_provider(Enzyme) # fake.organism_latin()  sounds like medicine enough
fake.add_provider(Bioseq) # fake.organism_latin()  sounds like medicine enough

TOTAL_ROOMS = 25
TOTAL_PATIENTS = 100
TOTAL_PHYSICIANS = 15
TOTAL_SURGEONS = 15
TOTAL_NURSES = 12

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

        # Create all beds and such
        for code, name in constants._UNITS:
            u = Unit(name=name, prefix=code)
            u.save()

            # Give all units 50 rooms
            for i in range(1, TOTAL_ROOMS):
                r = Room(number=i, unit=u)
                r.save()

                Bed(room=r, bed_letter="A").save()
                Bed(room=r, bed_letter="B").save()
                # Give even sides 3 beds, odd 2
                if i%2==0:
                    Bed(room=r, bed_letter="C").save()

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
            first_name="P.",
            last_name="Lastic",
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

    def create_medication1(self):
        medication1 = Medication(
            name = "Tylenol",
            code = 1001,
            available_qnty = 35,
            cost = 4.5,
            usage = """ Acetaminophen is used to relieve mild to moderate pain from headaches,
                             muscle aches, menstrual periods, colds and sore throats, toothaches,
                             and to reduce fever."""
        )
        medication1.save()
        print(f"Created Medication of '{medication1}'")
        return medication1

    def create_medication2(self):
        medication2 = Medication(
            name = "Advil",
            code = 1002,
            available_qnty = 46,
            cost = 6.25,
            usage = """ Ibuprofen is used to relieve pain from various conditions such as headache,
            dental pain, menstrual cramps, muscle aches, or arthritis. It is also used to reduce fever
            and to relieve minor aches and pain due to the common cold or flu."""
        )
        medication2.save()

        for _ in range(15):
            m = Medication(
                name=fake.amino_acid().full_name,
                code=random.randint(1000, 2000),
                available_qnty=random.randint(1,100),
                cost=float(random.randint(0,10)),
                usage=fake.paragraph(nb_sentences=5)
            )
            m.save()
        print(f"Created Medication of '{medication2}'")
        return medication2

    def create_many_nurses(self):
        """ Each nurse needs at least 5 patients """
        for i in range(TOTAL_NURSES):
            first = fake.first_name()
            n = Nurse(
                first_name=first,
                last_name=fake.last_name(),
                dob=fake.date(),
                gender="M" if 'e' in first else "F",
                address=fake.address(),
                phone=fake.phone_number(),
                ssn=fake.ssn(),
                grade=constants.NURSE_GRADES[random.randint(0, len(constants.NURSE_GRADES))-1][0],
                years_of_experience=random.randint(1,15),
                salary=random.randint(60_000, 180_000)
            )
            n.save()

    def create_many_patients(self):
        """ Create a bunch of patients """
        for i in range(TOTAL_PATIENTS):
            first = fake.first_name()
            p = Patient(
                first_name=first,
                last_name=fake.last_name(),
                dob=fake.date(),
                gender="M" if 'a' in first else "F",
                address=fake.address(),
                phone=fake.phone_number(),
                ssn=fake.ssn(),
                blood_type="an",
                blood_sugar=1.0,
                cholesterol_hdl=2.0,
                cholesterol_ldl=3.0,
                cholesterol_tri=4.0,
            )
            p.save()
            # Randomly admit some
            if random.randint(0, 1):
                p.bed = Bed.objects.filter(patient__isnull=True).order_by("?").first()
                p.assigned_nurse = Nurse.objects.order_by("?").first()
                p.save()

            # Randomly give some illnesses
            if random.randint(0, 1):
                name = fake.enzyme()
                illness = Illness(
                    name=name,
                    illness_code="".join([word[0] for word in name.split(" ")]),
                    description=fake.paragraph(nb_sentences=5)
                )
                illness.save()
                p.illnesses.add(illness)
                p.save()

            # Randomly give some allergies
            if random.randint(0, 1):
                name = fake.enzyme()
                allergy = Allergy(
                    name=name,
                    allergy_code="".join([word[0] for word in name.split(" ")]),
                    description=fake.paragraph(nb_sentences=5)
                )
                allergy.save()
                p.allergies.add(allergy)

                p.save()
                per = Perscriptions(
                    physician=Physician.objects.order_by("?").first(),
                    patient=p,
                    medication=Medication.objects.order_by("?").first(),
                    frequency=f"Take {random.randint(1,3)} daily",
                    dosage=f"{random.randint(100, 500)} mg"
                )
                per.save()

            if random.randint(0, 1):
                stype = SurgeryType.objects.order_by("?").first()
                eligable_nurses = [n for n in Nurse.objects.all() if n.can_perform(stype)]
                eligable_surgeons = [s for s in Surgeon.objects.all() if s.can_perform(stype)]
                if eligable_nurses and eligable_surgeons:
                    sur = Surgery(
                        date=fake.date(),
                        surgeon=eligable_surgeons[0],
                        nurse=eligable_nurses[0],
                        patient=p,
                        code="neu",
                        anatomical_location="Head",
                        category="h",
                        type=stype,
                        special_needs="None"
                    )
                    sur.save()

        print("Created 75 mock patients")

    def create_many_physicians(self):
        for _ in range(TOTAL_PHYSICIANS):
            first = fake.first_name()
            p = Physician(
                first_name=first,
                last_name=fake.last_name(),
                dob=fake.date(),
                gender="M" if 'c' in first else "F",
                address=fake.address(),
                phone=fake.phone_number(),
                ssn=fake.ssn(),
                specialty=constants.SPECIALTIES[random.randint(0, len(constants.SPECIALTIES)-1)][0],
                salary=random.randint(40_000, 180_000)
            )
            p.save()

    def create_many_surgeons(self):
        for _ in range(TOTAL_SURGEONS):
            first = fake.first_name()
            s = Surgeon(
                first_name=first,
                last_name=fake.last_name(),
                dob=fake.date(),
                gender="M" if 'c' in first else "F",
                address=fake.address(),
                phone=fake.phone_number(),
                ssn=fake.ssn(),
                specialty=constants.SPECIALTIES[random.randint(0, len(constants.SPECIALTIES)-1)][0],
                contract_length=random.randint(1, 10),
                contract_type="Type"+str(random.randint(1, 5))
            )
            s.save()


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

        # Create medication1 and medication2
        medication1 = self.create_medication1()
        medication2 = self.create_medication2()

        self.create_many_nurses()
        self.create_many_surgeons()
        self.create_many_physicians()
        self.create_many_patients()

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

        # # Give patient a bed and room, make sure admitted works
        # bed_names = {
        #     "gcu-1A": type(None), # Patient w/ no bed, before update this is null
        #     "gcu-2A": datetime, # Moving patient to new bed, has admitted time
        #     None: datetime, # Admitted time there from last, removing bed relation
        # }
        # for bed_name, admitted_type in bed_names.items():
        #     assert isinstance(general_patient.admission_date, admitted_type)
        #     bed = Bed.objects.get_bed_by_code(bed_name)
        #     general_patient.bed = bed
        #     general_patient.save()

        # Patient comes out in gcu-1A bed
        # general_patient.bed = Bed.objects.get_bed_by_code("gcu-1A")
        general_patient.save()

        call_command("runserver")