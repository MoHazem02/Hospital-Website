# Generated by Django 4.2.5 on 2023-12-22 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hospital', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='Specialization',
            field=models.CharField(choices=[('C', 'Cardiology'), ('D', 'Dentistry')], default='C', max_length=30),
        ),
        migrations.AddField(
            model_name='patient',
            name='history',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]