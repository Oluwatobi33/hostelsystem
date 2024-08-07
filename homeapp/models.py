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

class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Suite', 'Suite'),
    ]
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='rooms')
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    room_pic = models.ImageField(upload_to='rooms/', null=True, blank=True)


    def __str__(self):
        return f"{self.room_type} by {self.company.company_name}"

    
    is_active = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    is_created = models.DateTimeField(auto_now_add=True)
    is_updated = models.DateTimeField(auto_now=True)

    
class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.user} for {self.room}"

    def total_cost(self):
        return self.price  # Or any logic to calculate the total cost




class Receipt(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.FloatField()
    transaction_reference = models.CharField(max_length=100)
    date_generated = models.DateTimeField(auto_now_add=True)


class Payment(models.Model):
    amount = models.PositiveBigIntegerField()
    hostel_name = models.CharField(max_length=200, null=True, blank=True)
    room_type = models.CharField(max_length=200, null=True, blank=True)
    session = models.CharField(max_length=200, null=True, blank=True)
    room_upgrade = models.BooleanField(default=False)
    ref = models.CharField(max_length=210)
    user = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=True, blank=True)  # Ensure 'Candidate' model exists
    email = models.EmailField(max_length=200)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)


