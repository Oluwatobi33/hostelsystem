from django.db import models
import uuid


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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    USER_TYPE = (
        ('Undergraduate', 'Undergraduate'),
        ('Postgraduate', 'Postgraduate'),
        ('Jupeb', 'Jupeb'),
        ('Topup', 'Topup'),
        ('Parent', 'Parent'),
        ('Staff', 'Staff'),
        ('Others', 'Others'),
    )
    LEVEL = (
        ('100', '100'),
        ('200', '200'),
        ('300', '300'),
        ('400', '400'),
        ('Spill Over', 'Spill Over'),
        ('Jupeb', 'Jupeb'),
        ('Topup', 'Topup'),
        ('Others', 'Others'),
    )
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    ROOM_TYPE_CHOICES = [
        ('1', 'Single'),
        ('2', 'Double'),
        ('3', 'Suite'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room_type = models.CharField(max_length=2, choices=ROOM_TYPE_CHOICES)
    username = models.CharField(max_length=100, db_index=True)
    email = models.EmailField(max_length=200, unique=True, db_index=True)
    matric_number = models.EmailField(max_length=200, unique=True, null=True, blank=True)
    application_number = models.CharField(max_length=200, blank=True, null=True)
    user_type = models.CharField(max_length=200, choices=USER_TYPE, blank=True, null=True)
    gender = models.CharField(max_length=50, choices=GENDER, blank=True, null=True)
    level = models.CharField(max_length=50, choices=LEVEL, blank=True, null=True)
    phone_no = models.CharField(max_length=15, default="", blank=True, null=True)
    department = models.CharField(max_length=200, blank=True, null=True)
    programme = models.CharField(max_length=200, blank=True, null=True)

    is_active = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    is_created = models.DateTimeField(auto_now_add=True)
    is_updated = models.DateTimeField(auto_now=True)

    def get_room_type_display(self):
        return dict(self.ROOM_TYPE_CHOICES).get(self.room_type, 'Unknown')


class Booking(models.Model):
    user_id = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(default=False)
    username = models.CharField(max_length=255)
    matric_number = models.CharField(max_length=100)
    application_number = models.CharField(max_length=100)
    level = models.CharField(max_length=50)
    phone_no = models.CharField(max_length=15)
    department = models.CharField(max_length=100)
    programme = models.CharField(max_length=100)
    user_type = models.CharField(max_length=50)  # Add if needed

    def __str__(self):
        return self.username
class Receipt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.FloatField()
    transaction_reference = models.CharField(max_length=100)
    date_generated = models.DateTimeField(auto_now_add=True)

class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.PositiveBigIntegerField()
    hostel_name = models.CharField(max_length=200, null=True, blank=True)
    room_type = models.CharField(max_length=200, null=True, blank=True)
    session = models.CharField(max_length=200, null=True, blank=True)
    room_upgrade = models.BooleanField(default=False)
    ref = models.CharField(max_length=210)
    user = models.ForeignKey('Candidate', on_delete=models.CASCADE, null=True, blank=True)  # Ensure 'Candidate' model exists
    email = models.EmailField(max_length=200)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)
