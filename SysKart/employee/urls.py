from django.contrib import admin
from django.urls import path

from . import views

app_name = "employee"
urlpatterns = [
    path("", views.EmployeeView.as_view(), name="employeeview"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("attandance/", views.EmployeeAttandanceView.as_view(), name="attandance"),
    path("update/<int:pk>", views.ProfileUpdate.as_view(), name="update"),
]
