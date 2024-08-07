from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.db import IntegrityError
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ObjectDoesNotExist
import logging
from django.contrib.auth import logout as auth_logout
# from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import HttpResponse
from datetime import datetime
from django.contrib.auth.views import PasswordResetView
from .forms import CustomPasswordResetForm
from .models import *
from .forms import BookingForm
logger = logging.getLogger(__name__)
from .models import Room, Booking
from django.contrib import messages
from .forms import BookingForm
from django.contrib.auth.decorators import login_required
from .models import Room, Company
from .forms import RoomForm
import paystackapi
from paystackapi.transaction import Transaction


def index(request):
    return render(request, "index.html")

def index(request):
    rooms = Room.objects.all()
    return render(request, 'index.html', {'rooms': rooms})
 
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
                # Determine the user's role and get appropriate information
                if role == "Candidate" and user.role == "Candidate":
                    can = Candidate.objects.get(user_id=user)

                    # Populate session with user information
                    request.session['id'] = user.id
                    request.session['role'] = user.role
                    request.session['firstname'] = can.firstname
                    request.session['lastname'] = can.lastname
                    request.session['email'] = user.email
                    request.session['is_created'] = timezone.now().isoformat()  # Track when the session was created
                    request.session.set_expiry(60)  # Session expires in 1 minute

                    return redirect("index")

                elif role == "Company" and user.role == "Company":
                    comp = Company.objects.get(user_id=user)
                    
                    request.session['id'] = user.id
                    request.session['role'] = user.role
                    request.session['firstname'] = comp.firstname
                    request.session['lastname'] = comp.lastname
                    request.session['email'] = user.email
                    request.session['is_created'] = timezone.now().isoformat()  # Track when the session was created
                    request.session.set_expiry(1000)  # Session expires in 1 minute

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
    
# class BookingFormView(View):
#     def get(self, request, *args, **kwargs):
#         user_id = request.session.get('id')

#         if not user_id:
#             return redirect('login')

#         return render(request, 'booking_form.html')

#     def post(self, request, *args, **kwargs):
#         user_id = request.session.get('id')

#         if not user_id:
#             return redirect('login')

#         arrival = request.POST.get('arrival')
#         departure = request.POST.get('departure')

#         if not arrival or not departure:
#             return HttpResponse('Invalid input, please provide both arrival and departure dates.')

#         try:
#             check_in = datetime.strptime(arrival, "%Y-%m-%d")
#             check_out = datetime.strptime(departure, "%Y-%m-%d")
#         except ValueError:
#             return HttpResponse('Invalid date format, please use YYYY-MM-DD.')

#         total_charge = (check_out - check_in).days * 100  # Assume 100 per day

#         candidate = get_object_or_404(Candidate, user_id=user_id)

#         if Booking.objects.filter(email=candidate.email).exists():
#             return HttpResponse('A booking with this email already exists.')

#         try:
#             Booking.objects.create(
#                 user_id=candidate,
#                 firstname=candidate.firstname,
#                 lastname=candidate.lastname,
#                 email=candidate.email,
#                 phone=candidate.phone,
#                 address=candidate.address,
#                 city=candidate.city,
#                 state=candidate.state,
#                 arrival=check_in,
#                 departure=check_out,
#                 total_charge=total_charge
#             )
#         except IntegrityError:
#             return HttpResponse('A booking with this email already exists.')

#         return redirect('h')  # Change 'h' to the appropriate URL name

# def book_room(request):
#     user_id = request.session.get('id')
#     if not user_id:
#         return redirect('login')

#     try:
#         candidate = Candidate.objects.get(user_id=user_id)
#     except Candidate.DoesNotExist:
#         messages.error(request, "Candidate not found. Please contact support.")
#         return redirect('index')  # Redirect to home or an appropriate page

#     if request.method == 'POST':
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             booking = form.save(commit=False)  # Create an instance without saving
#             booking.user_id = candidate  # Associate the booking with the candidate
#             booking.save()  # Finally save the booking
#             messages.success(request, 'Booking created successfully!')
#             return redirect('paystack_payment', booking_id=booking.id)  # Redirect to a payment view
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         form = BookingForm()

#     return render(request, 'book_room.html', {'form': form})


# def booking_success(request, booking_id):
#     booking = get_object_or_404(Booking, id=booking_id)
#     context = {
#         'booking': booking
#     }
#     return render(request, 'booking_success.html', context)

def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'booking_success.html', {'booking': booking})

def paystack_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    candidate = booking.user_id  # Assuming the foreign key to Candidate is called user_id

    # Initialize the Paystack transaction
    response = Transaction.initialize(
        reference=f"payment_{booking.id}",
        amount=int(booking.total_cost() * 100),  # Amount in kobo
        email=candidate.email,
    )

    if response['status']:
        authorization_url = response['data']['authorization_url']
        return redirect(authorization_url)
    else:
        messages.error(request, 'Payment initialization failed.')
        return redirect('book_room')


def paystack_callback(request):
    reference = request.GET.get('reference')
    response = Transaction.verify(reference)
    
    if response['status']:
        booking_id = response['data']['metadata']['booking_id']
        booking = get_object_or_404(Booking, id=booking_id)
        booking.is_paid = True  # Mark the booking as paid
        booking.save()

        # Generate and save the receipt
        receipt = Receipt(
            booking=booking,
            amount=booking.total_cost(),  # Call the total_cost method
            transaction_reference=reference,
        )
        receipt.save()

        messages.success(request, 'Payment successful and receipt generated.')
        return redirect('booking_success', booking_id=booking.id)
    else:
        messages.error(request, 'Payment verification failed.')
        return redirect('book_room')
    


@login_required
def upgrade_room(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        booking.is_upgraded = True
        booking.save()
        return redirect('booking_success', booking_id=booking.id)
    return render(request, 'upgrade_room.html', {'booking': booking})



def UpdateBooking(request, pk):
    user = get_object_or_404(UserMaster, pk=pk)
    if request.method == 'POST':
        if user.role == 'Candidate':
            cand = Candidate.objects.get(user=user)
            cand.firstname = request.POST.get('firstname', cand.firstname)
            cand.lastname = request.POST.get('lastname', cand.lastname)
            cand.state = request.POST.get('state', cand.state)
            cand.city = request.POST.get('city', cand.city)
            cand.address = request.POST.get('address', cand.address)
            cand.phone = request.POST.get('phone', cand.phone)
            cand.arrival = request.POST.get('arrival', cand.arrival)
            cand.departure = request.POST.get('departure', cand.departure)
            
            logo_pic = request.FILES.get('logo_pic')
            if logo_pic:
                cand.logo_pic = logo_pic
            
            cand.save()
            return redirect('finalize_booking', pk=user.pk)
    else:
        cand = Candidate.objects.get(user=user)
    return render(request, "profile.html", {'use': user, 'cand': cand})


def dashboard(request):
    user_id = request.session.get('id')
    if user_id:
        user = UserMaster.objects.get(pk=user_id)
        return render(request, 'company/dashboard.html', {'user': user})
    else:
        return redirect('login')
    
# def UpdateCompanyProfilePage(request):
    # Fetch the user ID from the session
    user_id = request.session.get('id')
    if not user_id:
        return redirect('login')  # Redirect to login if user is not authenticated

    try:
        user = UserMaster.objects.get(id=user_id)
    except UserMaster.DoesNotExist:
        return redirect('login')  # Redirect to login if user is not found

    if user.role != 'Company':
        return redirect('login')  # Redirect to login if the user is not a company

    if request.method == 'POST':
        try:
            comp = Company.objects.get(user_id=user)
        except Company.DoesNotExist:
            return redirect('login')  # Redirect to login if company details are not found

        # Update company profile fields
        comp.firstname = request.POST.get('firstname', comp.firstname)
        comp.lastname = request.POST.get('lastname', comp.lastname)
        comp.company_name = request.POST.get('company_name', comp.company_name)
        comp.state = request.POST.get('state', comp.state)
        comp.city = request.POST.get('city', comp.city)
        comp.company_contact = request.POST.get('company_contact', comp.company_contact)
        comp.company_website = request.POST.get('company_website', comp.company_website)
        comp.description = request.POST.get('description', comp.description)
        comp.telephone = request.POST.get('telephone', comp.telephone)
        comp.address = request.POST.get('address', comp.address)
        
        if 'image' in request.FILES:
            comp.logo_pic = request.FILES['image']
            
        comp.save()
        return redirect('dashboard')  # Redirect to dashboard after saving
    else:
        try:
            comp = Company.objects.get(user_id=user)
        except Company.DoesNotExist:
            return redirect('login')  # Redirect to login if company details are not found

        return render(request, 'company/update_profile.html', {'use': user, 'comp': comp})


def UpdateCompanyProfilePage(request, pk):
    # Ensure the user is authenticated
    if 'id' not in request.session:
        return redirect('login')

    try:
        user = UserMaster.objects.get(pk=pk)
    except UserMaster.DoesNotExist:
        return redirect('login')  # Redirect to login if user is not found

    if user.role != 'Company':
        return redirect('login')  # Redirect to login if the user is not a company

    if request.method == 'POST':
        try:
            comp = Company.objects.get(user_id=user)
        except Company.DoesNotExist:
            return redirect('login')  # Redirect to login if company details are not found

        comp.firstname = request.POST.get('firstname', comp.firstname)
        comp.lastname = request.POST.get('lastname', comp.lastname)
        comp.email = request.POST.get('email', user.email)
        comp.state = request.POST.get('state', comp.state)
        comp.telephone = request.POST.get('telephone', comp.telephone)
        comp.company_contact = request.POST.get('company_contact', comp.company_contact)
        comp.address = request.POST.get('address', comp.address)
        comp.city = request.POST.get('city', comp.city)
        comp.description = request.POST.get('description', comp.description)

        if 'logo_pic' in request.FILES:
            comp.logo_pic = request.FILES['logo_pic']

        comp.save()

        messages.success(request, "Company profile updated successfully.")
        return redirect('companyProfile', pk=user.pk)

    comp = get_object_or_404(Company, user_id=user)
    return render(request, 'company/companyProfile.html', {'user': user, 'comp': comp})


def CompanyProfilePage(request,pk):
    user = UserMaster.objects.get(pk=pk)
    comp = Company.objects.get(user_id=user)
    return render(request, "./company/companyProfile.html", {'user': user, 'comp': comp})


def RoomPostList(request):
    all_job = Room.objects.all()
    return render( request, 'company/roompostlist.html', {'all_rooms':all_job})

def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    room.delete()
    messages.success(request, 'Room deleted successfully.')
    return redirect('roompostlist')



def edit_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == "POST":
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room updated successfully.')
            return redirect('roompostlist')
    else:
        form = RoomForm(instance=room)
    
    return render(request, 'company/edit_room.html', {'form': form, 'room': room})

def book_room(request):
    rooms = Room.objects.all()
    room = None
    form = None

    if 'room_id' in request.GET:
        room = get_object_or_404(Room, pk=request.GET['room_id'])
        form = BookingForm()

    if request.method == 'POST' and 'room_id' in request.POST:
        room = get_object_or_404(Room, pk=request.POST['room_id'])
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            
            # Check if the session contains the user id
            user_id = request.session.get('id')
            if user_id is None:
                return redirect('login')  # Or any other appropriate action

            # Retrieve the Candidate associated with the user_id
            try:
                booking.user = Candidate.objects.get(user_id=user_id)
            except Candidate.DoesNotExist:
                return redirect('login')  # Or any other appropriate action

            booking.room = room
            booking.save()
            room.available = False
            room.save()
            # Redirect to the booking success page with the booking_id
            return redirect('booking_success', booking_id=booking.id)

    if request.GET.get('room_type'):
        rooms = rooms.filter(room_type__icontains=request.GET['room_type'])

    return render(request, 'book_room.html', {'rooms': rooms, 'room': room, 'form': form})



# def book_room(request, room_id):
#     room = get_object_or_404(Room, pk=room_id)
#     if not room.available:
#         return redirect('search_rooms')

#     if request.method == 'POST':
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             booking = form.save(commit=False)
#             booking.user = request.user
#             booking.room = room
#             booking.save()
#             room.available = False
#             room.save()
#             return redirect('booking_success')
#     else:
#         form = BookingForm()

#     return render(request, 'book_room.html', {'form': form, 'room': room})


# def search_rooms(request):
#     rooms = Room.objects.all()
#     if request.GET:
#         room_type = request.GET.get('room_type')
#         if room_type:
#             rooms = rooms.filter(room_type__icontains=room_type)

#     return render(request, 'search_rooms.html', {'rooms': rooms})


def post_room(request):
    if request.method == "GET":
        # Ensure the user is authenticated
        if 'id' not in request.session:
            return redirect('login')  # Redirect to login page if the user is not authenticated

        # Get the logged-in user's company
        user_id = request.session.get('id')
        company = get_object_or_404(Company, user_id=user_id)
        
        # Pass the company information to the template
        return render(request, 'company/post_room.html', {'company_name': company.company_name})

    elif request.method == "POST":
        room_type = request.POST.get('room_type')
        description = request.POST.get('description')
        price = request.POST.get('price')
        available = 'available' in request.POST
        room_pic = request.FILES.get('room_pic')  # Get the uploaded image file

        # Ensure the user is authenticated
        if 'id' not in request.session:
            return redirect('login')  # Redirect to login page if the user is not authenticated

        # Get the logged-in user's company
        user_id = request.session.get('id')
        company = get_object_or_404(Company, user_id=user_id)

        # Create and save the room instance
        try:
            room = Room(
                room_type=room_type,
                description=description,
                price=price,
                company=company,
                available=available,
                room_pic=room_pic  # Save the image file
            )
            room.save()
            message = "Room posted successfully!"
            return render(request, 'company/post_room.html', {'company_name': company.company_name, 'message': message})
        except Exception as e:
            # Log the error or handle it appropriately
            print(f"Error saving room: {e}")
            return render(request, 'company/post_room.html', {
                'company_name': company.company_name,
                'error': 'An error occurred while saving the room.'
            })

# def post_room(request):
#     if request.method == "GET":
#         # Ensure the user is authenticated
#         user_id = request.session.get('id')
#         if not user_id:
#             return redirect('login')  # Redirect to login page if the user is not authenticated

#         # Get the logged-in user's company
#         user = get_object_or_404(UserMaster, id=user_id)
#         company = get_object_or_404(Company, user_id=user)
        
#         # Pass the company information to the template
#         return render(request, 'company/post_room.html', {'company_name': company.company_name})

#     elif request.method == "POST":
#         room_type = request.POST.get('room_type')
#         description = request.POST.get('description')
#         price = request.POST.get('price')
#         available = 'available' in request.POST

#         # Ensure the user is authenticated
#         user_id = request.session.get('id')
#         if not user_id:
#             return redirect('login')  # Redirect to login page if the user is not authenticated

#         # Get the logged-in user's company
#         user = get_object_or_404(UserMaster, id=user_id)
#         company = get_object_or_404(Company, user_id=user)

#         # Create and save the room instance
#         try:
#             room = Room(
#                 room_type=room_type,
#                 description=description,
#                 price=price,
#                 company=company,
#                 available=available
#             )
#             room.save()
#             message = "Room Posted successfully"
#             return render(request, "company/post_room.html", {"msg": message})

#             return redirect('dashboard')  # Redirect to a success page or another view
#         except Exception as e:
         
#             # Log the error or handle it appropriately
#             print(f"Error saving room: {e}")
#             return render(request, 'company/post_room.html', {
#                 'company_name': company.company_name,
#                 'error': 'An error occurred while saving the room.'
#             })



def logout_user(request):
    auth_logout(request)
    return redirect('login')