from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import User, Doctor, Patient, Message, Appointment, Article, Prescription
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
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    patient_query = "SELECT * FROM yourapp_patient WHERE username = %s LIMIT 1"
    patient = execute_query(patient_query, [request.user.username])

    doctors_query = "SELECT * FROM yourapp_doctor"
    doctors = execute_query(doctors_query)

    articles_query = "SELECT * FROM yourapp_article"
    articles = execute_query(articles_query)

    return render(request, "index.html", {"patient": patient[0], "doctors": doctors, "articles": articles})

def login_view(request):
    if request.method == "POST":
        username = request.POST["uname"]
        password = request.POST["password"]

        user_query = "SELECT * FROM yourapp_user WHERE username = %s AND password = %s LIMIT 1"
        user = execute_query(user_query, [username, password])

        if user:
            login(request, user[0])
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "patient-login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "patient-login.html")

def staff_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user_query = "SELECT * FROM yourapp_user WHERE username = %s AND password = %s LIMIT 1"
        user = execute_query(user_query, [username, password])

        if user:
            login(request, user[0])
            if username == 'admin':
                return HttpResponseRedirect(reverse("admin"))
            return HttpResponseRedirect(reverse("doctor"))
        else:
            return render(request, "staff-login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "staff-login.html")

# Implement similar raw SQL queries for other views...

