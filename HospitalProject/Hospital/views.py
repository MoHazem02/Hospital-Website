from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Doctor, Patient, Message, Appointment, Article, Prescription
from datetime import datetime 
import math


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "index.html", {"patient": Patient.objects.get(username=request.user.username), "doctors": Doctor.objects.all(), "articles": Article.objects.all()})


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["uname"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "patient-login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "patient-login.html")


def staff_login(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            if username == 'admin':
                return HttpResponseRedirect(reverse("admin"))
            return HttpResponseRedirect(reverse("doctor"))
        else:
            return render(request, "staff-login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "staff-login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        fName = request.POST["fname"]
        LName = request.POST["lname"]
        username = request.POST["uname"]
        email = request.POST["email"]
        gender = request.POST["gender"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            patient = Patient.objects.create_user(role="PATIENT", first_name=fName, last_name=LName, username= username, password=password, email=email, sex = "M" if gender == "Male" else "F")
            patient.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, patient)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")

def about(request):
    if request.method == "POST":
        pass
    else:
        return render(request, "about.html", {"patient": Patient.objects.get(username=request.user.username), "doctors": Doctor.objects.all()})


def service(request):
    if request.method == "POST":
        pass
    else:
        return render(request, "service.html", {"patient": Patient.objects.get(username=request.user.username)})


def pricing(request):
    if request.method == "POST":
        pass
    else:
        return render(request, "price.html", {"patient": Patient.objects.get(username=request.user.username), "doctors": Doctor.objects.all()})


@login_required    
def admin(request):
    if request.method == "POST":
        pass
    else:
        if request.user.username != 'admin':
            return HttpResponseRedirect(reverse("logout"))
        total_patients = Patient.objects.count()
        total_appointments = Appointment.objects.count()
        total_messages = Message.objects.count()
        return render(request, "admin.html", {"admin": User.objects.get(username=request.user.username), "messages":Message.objects.all(), "patients":total_patients,
                                              "appointments":total_appointments, "total_messages" : total_messages})
    

@login_required    
def doctor_view(request):
    if request.method == "POST":
        pass
    else:
        total_appointments = Appointment.objects.filter(doctor=Doctor.objects.get(username=request.user.username)).count()
        return render(request, "doctor.html", {"doctor": Doctor.objects.get(username=request.user.username), "appointments_count" : total_appointments, 
                                               "messages":Message.objects.filter(receiver=request.user.id), "appointments" :
                                                 Appointment.objects.filter(doctor=Doctor.objects.get(username=request.user.username))})
    

def admin_view_doctors(request):
    if request.method == 'POST':
        pass
    else:
        return render(request, "admin_view_doctors.html", {"doctors": Doctor.objects.all()})
    

def admin_add_staff(request):
    if request.method == 'POST':
        fName = request.POST["fname"]
        LName = request.POST["lname"]
        username = request.POST["uname"]
        email = request.POST["email"]
        Experience = request.POST["Experience"]
        department = request.POST.get('optionsRadios')
        profile_pic = request.POST.get('image_link')
        password = request.POST["password"]
        medicalDegree = request.POST.get('medicalDegree')
        workingShift = request.POST.get('workingShift')
        shiftOptions = {"Morning": 'M', "Evening": 'E', "Night": 'N'}
        chosenShift = shiftOptions[workingShift]
        # Attempt to create new user
        try:
            doctor = Doctor.objects.create_user(role="DOCTOR", first_name=fName, last_name=LName, username= username, password=password, email=email, experience = Experience,
                                                 profile_picture=profile_pic, specialization= department, medical_degree= medicalDegree , working_shift= chosenShift)
            doctor.save()
        except IntegrityError:
            return render(request, "admin_view_doctors.html")
        return HttpResponseRedirect(reverse("admin view doctors"))
    else:
        return render(request, "add-staff.html")
    

def make_appointment(request):
    if request.method == 'POST':
        doctor = Doctor.objects.get(id=request.POST.get('chosen_doctor'))
        scan = request.POST["scan"]
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        date = datetime.strptime(date_str, '%m/%d/%Y').date()
        time = datetime.strptime(time_str, '%I:%M %p').time()
        appointment = Appointment(patient=Patient.objects.get(username=request.user), doctor = doctor, appointment_date=date, appointment_time=time, image=scan)
        appointment.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "appointment.html", {"doctors" : Doctor.objects.all()})


def contact_us(request):
    if request.method == 'POST':
        message_subject = request.POST["message_subject"]
        message_body = request.POST['message_body']
        message = Message(sender=Patient.objects.get(username=request.user), receiver = User.objects.get(id=4), message_subject=message_subject, message=message_body)
        message.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, 'contact.html')


def blogs(request):
    return render(request, "blog.html", {"articles": Article.objects.all()})


def view_blog(request, id : int):
    return render(request, "detail.html", {"article" : Article.objects.get(id=id), "articles": Article.objects.all()})


def view_appointment(request, id : int):
    if request.method == 'POST':
        prescription_text = request.POST['prescription']
        patient = Patient.objects.get(id = id)
        prescription = Prescription(patient=patient, text=prescription_text, doctor=Doctor.objects.get(username=request.user))
        appointment = Appointment.objects.get(patient=Patient.objects.get(id = id))
        appointment.doctor.completed_appointments += 1
        appointment.done = True
        prescription.appointment = appointment
        appointment.save()
        prescription.save()
        return HttpResponseRedirect(reverse("doctor"))
    return render(request, "view_appointment.html", {"appointment" : Appointment.objects.get(id=id), "doctor": Doctor.objects.get(username=request.user.username)})


def view_calendar(request):
    if request.user.role == 'DOCTOR':
        return render(request, 'calendar.html', {"doctor" : Doctor.objects.get(username=request.user.username), 
                                                 "appointments" : Appointment.objects.filter(doctor=Doctor.objects.get(username=request.user.username)), "is_doctor":True})
    return render(request, 'calendar.html', {"is_doctor":False})


def history(request):
    return render(request, "history.html", {"completed_appointments" : Appointment.objects.filter(patient = Patient.objects.get(username = request.user.username), done=True)})


def rate_doctor(request, appointment_id : int):
    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        appointment = Appointment.objects.get(id = appointment_id)
        appointment.doctor.rating += rating
        appointment.doctor.rating /= math.ceil(appointment.doctor.completed_appointments)
        appointment.doctor.save()
    return HttpResponseRedirect(reverse("index"))
