from hospital.models.people import Patient, Surgeon, Physician, Nurse
from hospital.forms.base_form import BootstrapForm


class PatientForm(BootstrapForm):
    class Meta:
        model = Patient
        fields = [
            'first_name',
            'last_name',
            'dob',
            'gender',
            'address',
            'phone',
            'ssn',
            'allergies',
            'blood_type',
            'blood_sugar',
            'cholesterol_hdl',
            'cholesterol_ldl',
            'cholesterol_tri',
        ]

class PhysicianForm(BootstrapForm):
    class Meta:
        model = Physician
        fields = [
            'first_name',
            'last_name',
            'dob',
            'gender',
            'address',
            'phone',
            'ssn',
            'salary',
            'specialty'
        ]


class SurgeonForm(BootstrapForm):
    class Meta:
        model = Surgeon
        fields = [
            'first_name',
            'last_name',
            'dob',
            'gender',
            'address',
            'phone',
            'ssn',
            'specialty',
            'contract_length',
            'contract_type'
        ]


class NurseForm(BootstrapForm):
    class Meta:
        model = Nurse
        fields = [
            'first_name',
            'last_name',
            'dob',
            'gender',
            'address',
            'phone',
            'ssn',
            'grade',
            'years_of_experience',
            'salary'
        ]

class StaffToPatient(BootstrapForm):
    class Meta:
        model = Patient
        fields = [
            'allergies',
            'blood_type',
            'blood_sugar',
            'cholesterol_hdl',
            'cholesterol_ldl',
            'cholesterol_tri',
        ]