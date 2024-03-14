from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views import generic
from .forms import CustomUserCreationForm
from django.contrib import messages  # for messages
from django.contrib.auth import authenticate, logout, login



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


def login_user(request):
    member = request.user
    context = {'member': member}
    if request.method == 'POST':
        print('POST request received')
        username = request.POST['Username']
        password = request.POST['Password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print('Successful Login!')
            messages.success(request, 'Successful Login!')
            return render(request, 'dash/dashboard.html', context)  # Redirect to the home page
        else:
            print('ERROR: No username or password, please try again..')
            messages.error(request, 'ERROR: No username or password, please try again..')
            return render(request, 'accounts/home.html')  # Correct path to your login template
    else:
        print('ERROR: No username or password, please try again..')
        return render(request, 'accounts/home.html')  # Correct path to your login template


def logout_view(request):
    # Log the user out
    logout(request)
    print('Logout was Successful !')
    messages.success(request, 'Logout was Successful !')
    return redirect('accounts:landing_page')  # Redirect to the home page


def settings(request):
    # Fetch the user object from the database
    member = User.objects.get(username=request.user)

    # Pass the user object to the template
    context = {'member': member}
    return render(request, 'accounts/settings.html', context)
