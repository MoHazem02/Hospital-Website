# Generated by Django 4.2.5 on 2024-01-02 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hospital', '0006_doctor_experience'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='experience',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]
