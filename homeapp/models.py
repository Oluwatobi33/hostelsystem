from django.db import models


# Create your models here.
class UserMaster(models.Model):
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_created = models.DateTimeField(auto_now_add=True)
    is_updated = models.DateTimeField(auto_now_add=True)


class Candidate(models.Model):
    user_id = models.ForeignKey(UserMaster, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    dob = models.DateField(null=True, blank=True)  # Allow NULL values
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    special_requests = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to="img/candidate", blank=True, null=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class Company(models.Model):
    user_id = models.ForeignKey(UserMaster, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=50)
    company_contact = models.CharField(max_length=50)
    company_website = models.URLField(max_length=200)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    telephone = models.CharField(max_length=15)
    description = models.TextField()
    logo_pic = models.ImageField(upload_to="img/company")

    def __str__(self):
        return self.company_name


from django.db import models
from django.contrib.auth.models import User

class Booking(models.Model):
    user_id = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    arrival = models.DateField()
    departure = models.DateField()
    total_charge = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.firstname} booking from {self.arrival} to {self.departure}"
