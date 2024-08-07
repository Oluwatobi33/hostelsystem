from django.urls import path
from . import views
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth import views as auth_views
from .views import CustomPasswordResetView
from .views import *


urlpatterns = [
    path("", views.index, name='index'),
    path("signup/", views.signup, name='signup'),
    path("base/<int:pk>/", views.base, name='base'),
    path("register/", views.RegisterUser, name='register'),
    path('login/', views.LoginUser, name='login'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile/<int:pk>/', views.ProfilePage, name='profile'),
    path('updateprofile/<int:pk>/', views.UpdateProfile, name='updateprofile'),
    path('updatebooking/<int:pk>/', views.UpdateBooking, name='updatebooking'),
    path('upgrade-room/<int:booking_id>/', upgrade_room, name='upgrade_room'),
    path('booking-success/<int:booking_id>/', booking_success, name='booking_success'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/updatecompanyprofile/<int:pk>/', views.UpdateCompanyProfilePage, name='updatecompanyprofile'),
    path('roompostlist/', views.RoomPostList, name='roompostlist'),
    path('dashboard/companyProfile/<int:pk>/', views.CompanyProfilePage, name='companyProfile'),
    path('dashboard/post_room', views.post_room, name='post_room'),
    path('book-room/', views.book_room, name='book_room'),
    path('paystack_payment/<int:booking_id>/', views.paystack_payment, name='paystack_payment'),
    path('paystack-callback/', paystack_callback, name='paystack_callback'),
]
