from django.urls import path
from . import views
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth import views as auth_views
from .views import CustomPasswordResetView
from .views import BookingFormView


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
    path('book/', BookingFormView.as_view(), name='booking_form'),

]
