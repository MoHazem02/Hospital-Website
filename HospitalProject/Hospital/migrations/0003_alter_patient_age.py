# Generated by Django 4.2.5 on 2023-12-22 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hospital', '0002_doctor_specialization_patient_history'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]