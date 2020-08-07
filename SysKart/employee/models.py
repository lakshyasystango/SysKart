from django.contrib.auth.models import AbstractUser
from django.db import models


class EmployeeDetails(AbstractUser):
    name = models.CharField("Full Name", max_length=100)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.IntegerField(blank=True, null=True)
    password = models.CharField(max_length=20)
    salary = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.username


class EmployeeAttandance(models.Model):
    employee = models.ForeignKey(EmployeeDetails, on_delete=models.CASCADE)
    date = models.CharField(max_length=20)
    signin = models.TimeField(blank=True, null=True)
    signout = models.TimeField(blank=True, null=True)
    total_hours = models.CharField(max_length=20)

    def __str__(self):
        return str(self.employee)
