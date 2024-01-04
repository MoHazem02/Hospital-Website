from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    role = models.CharField(max_length=30, choices=[('ADMIN', 'Admin'), ('DOCTOR', 'Doctor'), ('PATIENT', 'Patient')], default='PATIENT')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30) 

class Doctor(User):
    medical_degree = models.CharField(max_length=30, choices=[('Specialist', 'Specialist'), ('Consultant', 'Consultant')], default='Specialist')
    working_shift = models.CharField(max_length=8, choices=[('M', 'Morning'), ('E', 'Evening'), ('N', 'Night')])
    profile_picture = models.CharField(max_length=512, null=True, blank=True)
    rating = models.FloatField(default=5.0, blank=True)
    specialization = models.CharField(max_length=30, choices=[('Cardiology', 'Cardiology'), ('Dentistry', 'Dentistry')], default='Cardiology')
    experience = models.CharField(max_length=400, null=True, blank=True)

    def __str__(self) -> str:
        return f"Dr. {self.first_name} {self.last_name}"

class Patient(User):
    sex = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    age = models.IntegerField(null=True, blank=True)
    history = models.CharField(max_length=255, null=True, blank=True)


    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
class Prescription(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    text = models.CharField(max_length=64, null=True, blank=False)

class Article(models.Model):
    subject = models.CharField(max_length=256)
    body = models.TextField()
    article_picture = models.CharField(max_length=512, null=True, blank=True)
    tag = models.CharField(max_length=64, null=True, blank=True)

class Message(models.Model):
    sender = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message_subject = models.CharField(max_length=128, null=True, blank=False)
    message = models.CharField(max_length=256, null=True, blank=False)

    def __str__(self):
        return self.message

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    image = models.ImageField(upload_to='patient_images/', null=True, blank=True)

    def __str__(self) ->str:
        return f"Appointment with Dr.{self.doctor} on {self.appointment_date} at {self.appointment_time}"
