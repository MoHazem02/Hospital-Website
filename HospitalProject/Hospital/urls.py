from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("staff", views.staff_login, name="staff_login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("about", views.about, name="about"),
    path("service", views.service, name="service"),
    path("pricing", views.pricing, name="pricing"),
    path("admin", views.admin, name="admin"),
    path("doctor", views.doctor_view, name='doctor'),
    path("staff/doctors", views.admin_view_doctors, name='admin view doctors'),
    path("staff/add-staff", views.admin_add_staff, name='admin add staff'),
]
