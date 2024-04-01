from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django import forms
from django.contrib.auth.models import User
from django.views import generic
from django.views.decorators.http import require_POST
from psycopg2 import IntegrityError

from .forms import CustomUserCreationForm, generate_unique_account_number
from django.contrib import messages  # for messages
from django.contrib.auth import authenticate, logout, login

from .models import Transaction, BankAccount, UserSetting
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError
from decimal import Decimal

from django.db.models.signals import post_save
from django.conf import settings
import logging
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from .models import BankAccount, Transaction
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import csv

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
    return render(request, 'accounts/home.html', {'member': member})


def dashboard(request):
    user = request.user
    user_settings = UserSetting.objects.get(user=request.user)
    monthly_income = user_settings.monthly_income
    annual_income = monthly_income * 12

    context = {
        'member': user,
        'settings': user_settings,
        'monthly_income': monthly_income,
        'annual_income': annual_income,
    }

    return render(request, 'accounts/dashboard.html', context)



# def dashboard(request):
#     monthly_income = 2000
#     annual_income = monthly_income * 12
#     member = request.user
#     return render(request, 'accounts/dashboard.html', {'member': member, 'monthly_income': monthly_income, 'annual_income': annual_income})


@require_POST
def generate_report(request):
    report_type = request.POST.get('reportType')

    if report_type == 'pdf':
        print('Generating PDF report')
        return generate_pdf(request)
    
    elif report_type == 'csv':
        print('Generating CSV report')
        return generate_csv(request)
    else:
        print('Invalid report type selected. Please try again.')
        return HttpResponse("Invalid report type selected. Please try again.")

def generate_pdf(request):
    user = request.user
    report_type = request.POST.get('reportType')
    user_account_number = request.POST.get('account_number')

    print(f'Generating a {report_type} report for account number: {user_account_number}')
    print(f'User: {user}')
    print(f'Report type: {report_type}')

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.drawString(100, 100, "Account Report.")
    pdf.showPage()

    print('PDF report was generated successfully')
    pdf.save()
    print('PDF report was saved successfully')

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="report.pdf")

def generate_csv(request):
    user = request.user
    report_type = request.POST.get('reportType')
    user_account_number = request.POST.get('account_number')
    transactions = BankAccount.objects.get(account_number=user_account_number).transactions.all()

    print(f'Generating a CSV report for account number: {user_account_number}')
    print(f'User: {user}')
    print(f'Transactions: {transactions}')


    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transaction_report.csv"'

    print('Writing CSV report')
    writer = csv.writer(response)

    
    writer.writerow(['Transaction ID', 'Type', 'Amount', 'Date'])

    print('Writing transactions to CSV')

    for transaction in transactions:
        writer.writerow([transaction.id, transaction.transaction_type, transaction.amount, transaction.date])

    print('CSV report was generated successfully')

    return response


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
