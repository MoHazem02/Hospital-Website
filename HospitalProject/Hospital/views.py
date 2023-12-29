from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Doctor, Patient
from django.shortcuts import get_object_or_404


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "index.html", {"patient": Patient.objects.get(username=request.user.username)})


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
            return HttpResponseRedirect(reverse("admin"))
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
            return render(request, "auctions/register.html", {
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
        return render(request, "about.html", {"patient": Patient.objects.get(username=request.user.username)})
    
def service(request):
    if request.method == "POST":
        pass
    else:
        return render(request, "service.html", {"patient": Patient.objects.get(username=request.user.username)})
    
def pricing(request):
    if request.method == "POST":
        pass
    else:
        return render(request, "price.html", {"patient": Patient.objects.get(username=request.user.username)})

@login_required    
def admin(request):
    if request.method == "POST":
        pass
    else:
        return render(request, "admin.html", {"admin": User.objects.get(username=request.user.username)})
    
@login_required    
def doctor_view(request):
    if request.method == "POST":
        pass
    else:
        return render(request, "doctor.html", {"doctor": Doctor.objects.get(username=request.user.username)})