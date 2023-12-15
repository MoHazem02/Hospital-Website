from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    role = models.CharField(max_length=30, choices=[('ADMIN', 'Admin'), ('DOCTOR', 'Doctor'), ('PATIENT', 'Patient')], default='PATIENT')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

class Doctor(User):
    medical_degree = models.CharField(max_length=30, choices=[('S', 'Specialist'), ('C', 'Consultant')], default='S')
    working_shift = models.CharField(max_length=8, choices=[('M', 'Morning'), ('E', 'Evening'), ('N', 'Night')])
    profile_picture = models.CharField(max_length=255, null=True, blank=True)
    rating = models.FloatField(default=5.0, blank=True)

    def __str__(self) -> str:
        return f"Dr. {self.first_name} {self.last_name}"

class Patient(User):
    sex = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    age = models.IntegerField()


    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
class Prescription(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    text = models.CharField(max_length=64)

class Article(models.Model):
    subject = models.CharField(max_length=64)
    body = models.TextField()

class Message(models.Model):
    sender = models.ForeignKey(Patient, on_delete=models.CASCADE)
    receiver = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    message = models.CharField(max_length=256)

    def __str__(self):
        return self.message

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()

    def __str__(self) ->str:
        return f"Appointment with Dr.{self.doctor} on {self.appointment_date} at {self.appointment_time}"
