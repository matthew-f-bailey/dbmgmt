# Generated by Django 4.1.7 on 2023-04-11 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assignedskills',
            old_name='surgeon',
            new_name='person',
        ),
        migrations.AlterField(
            model_name='skills',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]