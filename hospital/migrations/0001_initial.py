# Generated by Django 4.1.7 on 2023-05-02 01:56

import dirtyfields.dirtyfields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import hospital.models.base_model
import hospital.models.people
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Allergy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('allergy_code', models.CharField(max_length=10)),
                ('description', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Clinic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_length', models.PositiveIntegerField()),
                ('contract_type', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Illness',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('illness_code', models.CharField(max_length=10)),
                ('description', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Interactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('severity', models.CharField(choices=[('s', 'Severe Interaction'), ('m', 'Moderate Interaction'), ('l', 'Little Interaction')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('code', models.PositiveIntegerField()),
                ('available_qnty', models.PositiveIntegerField()),
                ('cost', models.FloatField()),
                ('usage', models.CharField(max_length=254)),
                ('interaction', models.ManyToManyField(through='hospital.Interactions', to='hospital.medication')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('emp_number', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('dob', models.DateField()),
                ('gender', models.CharField(choices=[('m', 'Male'), ('f', 'Female')], max_length=2)),
                ('address', models.CharField(max_length=254)),
                ('phone', models.CharField(max_length=30)),
                ('ssn', models.CharField(max_length=11)),
            ],
            bases=(models.Model, hospital.models.base_model.ShowAllDetailsMixin),
        ),
        migrations.CreateModel(
            name='Salaried',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salary', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(25000), django.core.validators.MaxValueValidator(300000)])),
            ],
        ),
        migrations.CreateModel(
            name='Skills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254)),
                ('prefix', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hospital.person')),
                ('blood_type', models.CharField(choices=[('ap', 'A Positive'), ('an', 'A Negative'), ('bp', 'B Positive'), ('bn', 'B Negative'), ('abp', 'AB Positive'), ('abn', 'AB Negative'), ('op', 'O Positive'), ('on', 'O Negative')], max_length=30)),
                ('blood_sugar', models.FloatField()),
                ('cholesterol_hdl', models.FloatField()),
                ('cholesterol_ldl', models.FloatField()),
                ('cholesterol_tri', models.FloatField()),
                ('admission_date', models.DateField(null=True)),
                ('allergies', models.ManyToManyField(blank=True, to='hospital.allergy')),
            ],
            bases=('hospital.person', dirtyfields.dirtyfields.DirtyFieldsMixin),
        ),
        migrations.CreateModel(
            name='Physician',
            fields=[
                ('salaried_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='hospital.salaried')),
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hospital.person')),
                ('specialty', models.CharField(choices=[('podiatry', 'Podiatry'), ('general', 'General Practice'), ('optometry', 'Optometry')], max_length=50)),
            ],
            bases=('hospital.person', 'hospital.salaried'),
        ),
        migrations.CreateModel(
            name='SkilledPerson',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hospital.person')),
            ],
            bases=('hospital.person',),
        ),
        migrations.CreateModel(
            name='SurgeryType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('requirements', models.ManyToManyField(to='hospital.skills')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField()),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.unit')),
            ],
        ),
        migrations.AddField(
            model_name='interactions',
            name='medication1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='first_med', to='hospital.medication'),
        ),
        migrations.AddField(
            model_name='interactions',
            name='medication2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='second_med', to='hospital.medication'),
        ),
        migrations.CreateModel(
            name='Bed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bed_letter', models.CharField(max_length=1)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.room')),
            ],
        ),
        migrations.CreateModel(
            name='Nurse',
            fields=[
                ('salaried_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='hospital.salaried')),
                ('skilledperson_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hospital.skilledperson')),
                ('grade', models.CharField(choices=[('a', 'A'), ('b', 'B'), ('c', 'C')], max_length=10)),
                ('years_of_experience', models.PositiveIntegerField()),
            ],
            bases=('hospital.skilledperson', 'hospital.salaried'),
        ),
        migrations.CreateModel(
            name='Surgeon',
            fields=[
                ('contract_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='hospital.contract')),
                ('skilledperson_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hospital.skilledperson')),
                ('specialty', models.CharField(choices=[('podiatry', 'Podiatry'), ('general', 'General Practice'), ('optometry', 'Optometry')], max_length=254)),
            ],
            bases=('hospital.skilledperson', 'hospital.contract'),
        ),
        migrations.CreateModel(
            name='Perscriptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frequency', models.CharField(max_length=100)),
                ('dosage', models.CharField(max_length=100)),
                ('medication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.medication')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.patient')),
                ('physician', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital.physician')),
            ],
        ),
        migrations.AddField(
            model_name='patient',
            name='bed',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital.bed'),
        ),
        migrations.AddField(
            model_name='patient',
            name='illnesses',
            field=models.ManyToManyField(blank=True, to='hospital.illness'),
        ),
        migrations.AddField(
            model_name='patient',
            name='pcp',
            field=models.ForeignKey(blank=True, default=hospital.models.people.Physician.get_chief_of_staff, null=True, on_delete=models.SET(hospital.models.people.get_chief_of_staff), to='hospital.physician'),
        ),
        migrations.AlterUniqueTogether(
            name='interactions',
            unique_together={('medication1', 'medication2')},
        ),
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.patient')),
                ('physician', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.physician')),
            ],
        ),
        migrations.CreateModel(
            name='Surgery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=30)),
                ('code', models.CharField(choices=[('neu', 'Neurosurgery'), ('pod', 'Podiatric Surgery')], max_length=5)),
                ('anatomical_location', models.CharField(choices=[('foot', 'Foot'), ('head', 'Head')], max_length=100)),
                ('category', models.CharField(choices=[('h', 'Requires Hospitalization'), ('o', 'Outpatient')], max_length=100)),
                ('special_needs', models.CharField(max_length=100)),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital.surgerytype')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.patient')),
                ('nurse', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital.nurse')),
                ('surgeon', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital.surgeon')),
            ],
        ),
        migrations.AddField(
            model_name='patient',
            name='assigned_nurse',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital.nurse'),
        ),
        migrations.CreateModel(
            name='AssignedSkills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.skills')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.skilledperson')),
            ],
            options={
                'unique_together': {('person', 'skill')},
            },
        ),
    ]
