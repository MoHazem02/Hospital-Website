from django.contrib import admin
from .models import Doctor, Patient, Prescription, Message, Article, Appointment, User

# Register your models here.
admin.site.register(User)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Prescription)
admin.site.register(Message)
admin.site.register(Article)
admin.site.register(Appointment)