from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import Hospital, Doctor, Patient, Message, Appointment, Article, Prescription
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from django.conf import settings  
from googleapiclient.discovery import build
import math

def execute_query(query, params=None):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()

def index(request):
    if not request.Hospital.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    patient_query = "SELECT * FROM Hospital_patient WHERE Hospitalname = %s LIMIT 1"
    patient = execute_query(patient_query, [request.Hospital.Hospitalname])

    doctors_query = "SELECT * FROM Hospital_doctor"
    doctors = execute_query(doctors_query)

    articles_query = "SELECT * FROM Hospital_article"
    articles = execute_query(articles_query)

    return render(request, "index.html", {"patient": patient[0], "doctors": doctors, "articles": articles})

def login_view(request):
    if request.method == "POST":
        Hospitalname = request.POST["uname"]
        password = request.POST["password"]

        Hospital_query = "SELECT * FROM Hospital_Hospital WHERE Hospitalname = %s AND password = %s LIMIT 1"
        Hospital = execute_query(Hospital_query, [Hospitalname, password])

        if Hospital:
            login(request, Hospital[0])
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "patient-login.html", {
                "message": "Invalid Hospitalname and/or password."
            })
    else:
        return render(request, "patient-login.html")

def staff_login(request):
    if request.method == "POST":
        Hospitalname = request.POST["Hospitalname"]
        password = request.POST["password"]

        Hospital_query = "SELECT * FROM Hospital_Hospital WHERE Hospitalname = %s AND password = %s LIMIT 1"
        Hospital = execute_query(Hospital_query, [Hospitalname, password])

        if Hospital:
            login(request, Hospital[0])
            if Hospitalname == 'admin':
                return HttpResponseRedirect(reverse("admin"))
            return HttpResponseRedirect(reverse("doctor"))
        else:
            return render(request, "staff-login.html", {
                "message": "Invalid Hospitalname and/or password."
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
        Hospitalname = request.POST["uname"]
        email = request.POST["email"]
        gender = request.POST["gender"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        try:
            patient_query = "INSERT INTO Hospital_patient (role, first_name, last_name, Hospitalname, password, email, sex) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            execute_query(patient_query, ["PATIENT", fName, LName, Hospitalname, password, email, "M" if gender == "Male" else "F"])
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Hospitalname already taken."
            })

        Hospital_query = "SELECT * FROM Hospital_Hospital WHERE Hospitalname = %s LIMIT 1"
        Hospital = execute_query(Hospital_query, [Hospitalname])

        login(request, Hospital[0])
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")


def about(request):
    if request.method == "POST":
        pass
    else:
        patient_query = "SELECT * FROM Hospital_patient WHERE Hospitalname = %s LIMIT 1"
        patient = execute_query(patient_query, [request.Hospital.Hospitalname])

        doctors_query = "SELECT * FROM Hospital_doctor"
        doctors = execute_query(doctors_query)

        return render(request, "about.html", {"patient": patient[0], "doctors": doctors})

def service(request):
    if request.method == "POST":
        pass
    else:
        patient_query = "SELECT * FROM Hospital_patient WHERE Hospitalname = %s LIMIT 1"
        patient = execute_query(patient_query, [request.Hospital.Hospitalname])

        return render(request, "service.html", {"patient": patient[0]})

def pricing(request):
    if request.method == "POST":
        pass
    else:
        patient_query = "SELECT * FROM Hospital_patient WHERE Hospitalname = %s LIMIT 1"
        patient = execute_query(patient_query, [request.Hospital.Hospitalname])

        doctors_query = "SELECT * FROM Hospital_doctor"
        doctors = execute_query(doctors_query)

        return render(request, "price.html", {"patient": patient[0], "doctors": doctors})

@login_required
def admin(request):
    if request.method == "POST":
        pass
    else:
        if request.Hospital.Hospitalname != 'admin':
            return HttpResponseRedirect(reverse("logout"))

        total_patients_query = "SELECT COUNT(*) FROM Hospital_patient"
        total_patients = execute_query(total_patients_query)[0][0]

        total_appointments_query = "SELECT COUNT(*) FROM Hospital_appointment"
        total_appointments = execute_query(total_appointments_query)[0][0]

        total_messages_query = "SELECT COUNT(*) FROM Hospital_message"
        total_messages = execute_query(total_messages_query)[0][0]

        return render(request, "admin.html", {"admin": request.Hospital, "messages": total_messages, "patients": total_patients,
                                              "appointments": total_appointments})

@login_required
def doctor_view(request):
    if request.method == "POST":
        pass
    else:
        total_appointments_query = "SELECT COUNT(*) FROM Hospital_appointment WHERE doctor_id = %s"
        total_appointments = execute_query(total_appointments_query, [request.Hospital.id])[0][0]

        return render(request, "doctor.html", {"doctor": request.Hospital, "appointments_count": total_appointments,
                                               "messages": execute_query("SELECT * FROM Hospital_message WHERE receiver_id = %s", [request.Hospital.id]),
                                               "appointments": execute_query("SELECT * FROM Hospital_appointment WHERE doctor_id = %s", [request.Hospital.id])})


def admin_view_doctors(request):
    if request.method == 'POST':
        pass
    else:
        doctors_query = "SELECT * FROM Hospital_doctor"
        doctors = execute_query(doctors_query)

        return render(request, "admin_view_doctors.html", {"doctors": doctors})

def admin_add_staff(request):
    if request.method == 'POST':
        fName = request.POST["fname"]
        LName = request.POST["lname"]
        Hospitalname = request.POST["uname"]
        email = request.POST["email"]
        Experience = request.POST["Experience"]
        department = request.POST.get('optionsRadios')
        profile_pic = request.POST.get('image_link')
        password = request.POST["password"]
        medicalDegree = request.POST.get('medicalDegree')
        workingShift = request.POST.get('workingShift')
        shiftOptions = {"Morning": 'M', "Evening": 'E', "Night": 'N'}
        chosenShift = shiftOptions[workingShift]

        try:
            doctor_query = "INSERT INTO Hospital_doctor (role, first_name, last_name, Hospitalname, password, email, experience, profile_picture, specialization, medical_degree, working_shift) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            execute_query(doctor_query, ["DOCTOR", fName, LName, Hospitalname, password, email, Experience, profile_pic, department, medicalDegree, chosenShift])
        except IntegrityError:
            return render(request, "admin_view_doctors.html")

        return HttpResponseRedirect(reverse("admin view doctors"))
    else:
        return render(request, "add-staff.html")

def make_appointment(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('chosen_doctor')
        scan = request.POST["scan"]
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        date = datetime.strptime(date_str, '%m/%d/%Y').date()
        time = datetime.strptime(time_str, '%I:%M %p').time()

        appointment_query = "INSERT INTO Hospital_appointment (patient_id, doctor_id, appointment_date, appointment_time, image) VALUES (%s, %s, %s, %s, %s)"
        execute_query(appointment_query, [request.Hospital.id, doctor_id, date, time, scan])

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "appointment.html", {"doctors": execute_query("SELECT * FROM Hospital_doctor")})


def contact_us(request):
    if request.method == 'POST':
        message_subject = request.POST["message_subject"]
        message_body = request.POST['message_body']

        message_query = "INSERT INTO Hospital_message (sender_id, receiver_id, message_subject, message) VALUES (%s, %s, %s, %s)"
        execute_query(message_query, [request.Hospital.id, 4, message_subject, message_body])

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, 'contact.html')

def blogs(request):
    articles_query = "SELECT * FROM Hospital_article"
    articles = execute_query(articles_query)

    return render(request, "blog.html", {"articles": articles})

def view_blog(request, id: int):
    article_query = "SELECT * FROM Hospital_article WHERE id = %s LIMIT 1"
    article = execute_query(article_query, [id])

    articles_query = "SELECT * FROM Hospital_article"
    articles = execute_query(articles_query)

    return render(request, "detail.html", {"article": article[0], "articles": articles})

def view_appointment(request, id: int):
    if request.method == 'POST':
        prescription_text = request.POST['prescription']
        patient_query = "SELECT * FROM Hospital_patient WHERE id = %s LIMIT 1"
        patient = execute_query(patient_query, [id])

        prescription_query = "INSERT INTO Hospital_prescription (patient_id, text, doctor_id) VALUES (%s, %s, %s)"
        execute_query(prescription_query, [patient[0][0], prescription_text, request.Hospital.id])

        appointment_query = "UPDATE Hospital_appointment SET done = TRUE WHERE patient_id = %s"
        execute_query(appointment_query, [patient[0][0]])

        return HttpResponseRedirect(reverse("doctor"))
    
    appointment_query = "SELECT * FROM Hospital_appointment WHERE id = %s LIMIT 1"
    appointment = execute_query(appointment_query, [id])
    
    return render(request, "view_appointment.html", {"appointment": appointment[0], "doctor": request.Hospital})

def view_calendar(request):
    if request.Hospital.role == 'DOCTOR':
        doctor_query = "SELECT * FROM Hospital_doctor WHERE id = %s LIMIT 1"
        doctor = execute_query(doctor_query, [request.Hospital.id])

        appointments_query = "SELECT * FROM Hospital_appointment WHERE doctor_id = %s"
        appointments = execute_query(appointments_query, [request.Hospital.id])

        return render(request, 'calendar.html', {"doctor": doctor[0], "appointments": appointments, "is_doctor": True})
    return render(request, 'calendar.html', {"is_doctor": False})

def history(request):
    completed_appointments_query = "SELECT * FROM Hospital_appointment WHERE patient_id = %s AND done = TRUE"
    completed_appointments = execute_query(completed_appointments_query, [request.Hospital.id])

    return render(request, "history.html", {"completed_appointments": completed_appointments})

def rate_doctor(request, appointment_id: int):
    if request.method == 'POST':
        rating = int(request.POST.get('rating'))

        doctor_query = "SELECT * FROM Hospital_doctor WHERE id = %s LIMIT 1"
        doctor = execute_query(doctor_query, [request.Hospital.id])

        completed_appointments_query = "SELECT * FROM Hospital_appointment WHERE id = %s AND done = TRUE LIMIT 1"
        completed_appointment = execute_query(completed_appointments_query, [appointment_id])

        new_rating = (doctor[0][8] * doctor[0][9] + rating) / (doctor[0][9] + 1)

        update_doctor_query = "UPDATE Hospital_doctor SET rating = %s, completed_appointments = %s WHERE id = %s"
        execute_query(update_doctor_query, [new_rating, doctor[0][9] + 1, request.Hospital.id])

    return HttpResponseRedirect(reverse("index"))










