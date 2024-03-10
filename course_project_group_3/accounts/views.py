from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django import forms
from django.contrib.auth.models import User
from django.views import generic
from .forms import CustomUserCreationForm


# Create your views here.


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


# @login_required
def wallet(request):
    # Fetch the user object from the database
    member = request.user

    # Pass the user object to the template
    context = {'member': member}

    return render(request, 'accounts/wallet.html', context)


def profile(request):
    # Fetch the user object from the database
    member = User.objects.get(username=request.user)

    # Pass the user object to the template
    context = {'member': member}
    return render(request, 'accounts/profile.html', context)


def register(request):
    return render(request, 'accounts/register.html')


def login(request):
    return render(request, 'accounts/login.html')


def settings(request):
    # Fetch the user object from the database
    member = User.objects.get(username=request.user)

    # Pass the user object to the template
    context = {'member': member}
    return render(request, 'accounts/settings.html', context)
