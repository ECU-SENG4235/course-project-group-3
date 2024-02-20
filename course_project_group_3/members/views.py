from django.contrib.auth import logout
from django.shortcuts import render


# Create your views here.


# This function is a view for the index page of the dashboard, it's not needed for the project.
def index(request):
    return render(request, 'dashboard/members_index.html')


def sign_in(request):
    # TODO:  ST-67  Implement sign in logic
    return render(request, 'dashboard/sign_in.html')


def sign_up(request):
    # TODO:  ST-67  Implement sign up logic
    return render(request, 'dashboard/sign_up.html')


def sign_out(request):
    # Sign user out using django.contrib.auth.logout
    logout(request)
    return render(request, 'dashboard/sign_out.html')