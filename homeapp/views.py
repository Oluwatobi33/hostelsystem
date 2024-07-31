from django.shortcuts import render, redirect
from .models import *
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ObjectDoesNotExist
import logging
from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import HttpResponse
from datetime import datetime


logger = logging.getLogger(__name__)


def index(request):
    return render(request, "index.html")
 
def base(request):
    return render(request, 'base.html')

def signup(request):
    return render(request, "signup.html")

def login(request):
    return render(request, "login.html")

def LoginUser(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = UserMaster.objects.get(email=email)
            
            if user.password == password:
                if role == "Candidate" and user.role == "Candidate":
                    can = Candidate.objects.get(user_id=user)
                    request.session['id'] = user.id
                    request.session['role'] = user.role
                    request.session['firstname'] = can.firstname
                    request.session['lastname'] = can.lastname
                    request.session['email'] = user.email
                    request.session['password'] = user.password
                    request.session['is_created'] = str(timezone.now())
                    request.session.set_expiry(60)  # Session expires in 1 minute
                    return redirect("index")
                elif role == "Company" and user.role == "Company":
                    comp = Company.objects.get(user_id=user)
                    request.session['id'] = user.id
                    request.session['role'] = user.role
                    request.session['firstname'] = comp.firstname
                    request.session['lastname'] = comp.lastname
                    request.session['email'] = user.email
                    request.session['password'] = user.password
                    request.session['is_created'] = str(timezone.now())
                    request.session.set_expiry(60)  # Session expires in 1 minute
                    return redirect("dashboard")
                else:
                    message = "Role mismatch"
                    return render(request, "login.html", {"msg": message})
            else:
                message = "Password does not match"
                return render(request, "login.html", {"msg": message})
        
        except UserMaster.DoesNotExist:
            message = "User does not exist"
            return render(request, "login.html", {"msg": message})
    
    return render(request, "login.html")



# views.py
from django.contrib.auth.views import PasswordResetView
from .forms import CustomPasswordResetForm

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm


def RegisterUser(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        fname = request.POST.get('firstname')
        lname = request.POST.get('lastname')

        print(f"Role: {role}, Email: {email}")
        user = UserMaster.objects.filter(email=email)
        if user.exists():
            message = "User already exists"
            print(message)
            return render(request, 'signup.html', {'msg': message})
        else:
            if password == cpassword:
                newuser = UserMaster.objects.create(role=role,  email=email, password=password)
                if role == "Candidate":
                    newcand = Candidate.objects.create(user_id=newuser, firstname=fname, lastname=lname)
                elif role == "Company":
                    newcomp = Company.objects.create(user_id=newuser, firstname=fname, lastname=lname)
                return redirect('login')
            else:
                message = "Passwords do not match"
                print(message)
                return render(request, 'signup.html', {'msg': message})
    else:
        return render(request, 'signup.html')
    

def  ProfilePage(request, pk):
    try:
        user = UserMaster.objects.get(id=pk)
        candidate = Candidate.objects.get(user_id=user.id)
    except ObjectDoesNotExist:
        return redirect('login')  # or any other error handling

    return render(request, 'profile.html', {'user': user, 'cand': candidate})


def UpdateProfile(request, pk):
    user_id = request.session.get('id')
    if not user_id:
        return redirect('login')

    if request.method == 'POST':
        try:
            can = Candidate.objects.get(user_id=user_id)
        except ObjectDoesNotExist:
            return redirect('error')

        can.firstname = request.POST.get('firstname')
        can.lastname = request.POST.get('lastname')
        can.email = request.POST.get('email')
        can.phone = request.POST.get('phone')
        can.address = request.POST.get('address')
        can.city = request.POST.get('city')
        can.state = request.POST.get('state')
        can.dob = request.POST.get('dob')
        can.gender = request.POST.get('gender')
        can.special_requests = request.POST.get('special_requests')
        can.profile_pic = request.FILES.get('profile_pic') if request.FILES.get('profile_pic') else can.profile_pic

        try:
            can.save()
            message = "Profile updated successfully."
            return render(request, "profile.html", {"msg": message, "cand": can, "user": can.user_id})
        except Exception as e:
            logger.error(f"Error updating profile: {e}")
            message = "There was an error updating your profile. Please try again."
            return render(request, "profile.html", {"msg": message, "cand": can, "user": can.user_id})

    try:
        cand = Candidate.objects.get(user_id=user_id)
        return render(request, "profile.html", {"cand": cand, "user": cand.user_id})
    except ObjectDoesNotExist:
        return redirect('error')


def BookingFormView(View):
    user_id = request.session.get('id')

    if not user_id:
        return redirect('login')
    


    def post(self, request, *args, **kwargs):
        arrival = request.POST.get('arrival')
        departure = request.POST.get('departure')
        
        if not arrival or not departure:
            return HttpResponse('Invalid input, please provide both arrival and departure dates.')

            try:
                check_in = datetime.strptime(arrival, "%Y-%m-%d")
                check_out = datetime.strptime(departure, "%Y-%m-%d")
            except ValueError:
                return HttpResponse('Invalid date format, please use YYYY-MM-DD.')

            # Save data to session
            request.session['check_in'] = check_in.strftime("%Y-%m-%d")
            request.session['check_out'] = check_out.strftime("%Y-%m-%d")

            # Implement the logic for calculating the total charge
            # and save to session or handle accordingly
   
        return redirect('h')
