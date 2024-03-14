from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django import forms
from django.contrib.auth.models import User
from django.views import generic
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login as auth_login


# Create your views here.


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


def base(request):
    member = request.user
    context = {'member': member}
    return render(request, 'accounts/base.html', context)


# Will serve as the landing page for unauthenticated users
def landing_page(request):
    member = request.user
    context = {'member': member}
    return render(request, 'accounts/home.html', context)


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
    username = request.POST.get("username")
    password = request.POST.get("password")

    if username is None or password is None:
        # TODO: Return an 'invalid username or password' error message.
        pass

    try:
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            # TODO: Redirect to a success page.
            # return redirect('success_page')
        else:
            # TODO: Return an 'invalid login' error message.
            pass
    except Exception as e:
        # TODO Handle exception here, possibly return an 'internal server error' message.
        pass

    return render(request, 'accounts/login.html')


def logout(request):
    logout(request)
    # Redirect to a success page.
    return render(request, 'accounts/logout.html')


def settings(request):
    # Fetch the user object from the database
    member = User.objects.get(username=request.user)

    # Pass the user object to the template
    context = {'member': member}
    return render(request, 'accounts/settings.html', context)
