# Generated by Django 4.2.5 on 2024-01-01 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hospital', '0004_remove_doctor_specialization_doctor_specialization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='medical_degree',
            field=models.CharField(choices=[('Specialist', 'Specialist'), ('Consultant', 'Consultant')], default='Specialist', max_length=30),
        ),
    ]
