import csv
from datetime import datetime
from enum import member
import io
from msilib import Table
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from django.http import HttpResponse, FileResponse
import io
import csv
from .models import Transaction, BankAccount
from .models import Transaction
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views import generic
from django.views.decorators.http import require_POST
from psycopg2 import IntegrityError

from .forms import CustomUserCreationForm, SpendingLimitForm, generate_unique_account_number
from django.contrib import messages  # for messages
from django.contrib.auth import authenticate, logout, login

from .models import Transaction, BankAccount, UserSetting
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from decimal import Decimal

from django.db.models.signals import post_save
from django.conf import settings
import logging
from reportlab.lib import colors
from reportlab.platypus import Spacer
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.platypus import TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from django.views.decorators.http import require_POST
import io
import csv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse, FileResponse
from .models import Transaction, BankAccount
from django.views.decorators.http import require_POST
import re
import json

from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime
from dateutil.relativedelta import relativedelta


logger = logging.getLogger(__name__)  # Set up basic logging


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
    bank_accounts = BankAccount.objects.filter(user=request.user)
    monthly_income = user_settings.monthly_income
    annual_income = monthly_income * 12
    accounts = [{'id': account.id, 'last_four': str(account.account_number)[-4:]} for account in bank_accounts]

    form = SpendingLimitForm(request.user)

    total = 0

    #Check if budget account has been set
    if user_settings.budget_account is not None:
        
        #check if there are any transactions in the budget account
        if Transaction.objects.filter(account=user_settings.budget_account).count() != 0:

            for transaction in Transaction.objects.filter(account=user_settings.budget_account, transaction_type='withdrawal'):
                total += transaction.amount

            percent = total / user_settings.budget_account.spending_limit
            percent = percent * 100
            
    else:
        percent = 0







    # #Creating test transactions to check if the chart works
    # # Fetch the user
    # user = User.objects.get(username='jerry')  # replace 'username_here' with the actual username
    # first_account = user.bank_accounts.first()

    # # Get the current date
    # now = timezone.now()

    # # Create transactions for the past three months
    # for months_ago in range(3, 0, -1):
    #     # Calculate the date for the required number of months ago
    #     date = now - relativedelta(months=months_ago)
    #     # Set the date to the first day of the month
    #     date = date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    #     # Create the transaction
    #     transaction = Transaction(account=first_account, transaction_type='withdrawal', timestamp=date, amount=50.0)
    #     transaction.save()

    #     print(transaction.timestamp)















    #Add spending limit form
    if request.method == 'POST':
        form = SpendingLimitForm(request.user, request.POST)
        if form.is_valid():
            account = form.cleaned_data['account']
            account.spending_limit = form.cleaned_data['spending_limit']
            user_settings.budget_account = account
            user_settings.save()
            account.save()
            return redirect('accounts:dashboard')
    else:
        form = SpendingLimitForm(request.user)

    #Creating values for charts
    labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    data = []  # Initialize an empty list to store the sum of transactions for each month

    current_year = timezone.now().year

    withdrawal_transactions = []
    for month in range(1, 13):
        transactions = Transaction.objects.filter(account__user=user,transaction_type='withdrawal', timestamp__year=current_year, timestamp__month=month)
        withdrawal_transactions.extend(transactions)

        if transactions.exists():
            # Calculate the sum of transactions for the current month
            month_sum = sum(transaction.amount for transaction in transactions)
            data.append(month_sum)
        else:
            data.append(0)
    
    data = [float(x) for x in data]

    #Convert data to json to pass to template
    data = json.dumps(data)
    labels = json.dumps(labels)


    context = {
        'member': user,
        'settings': user_settings,
        'monthly_income': monthly_income,
        'annual_income': annual_income,
        'accounts': accounts,
        'form': form,
        'percent': percent,
        'labels': labels,
        'data': data
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
        return generate_pdf_report(request)
    elif report_type == 'csv':
        print('Generating CSV report')
        return generate_csv_report(request)
    else:
        print('Invalid report type selected. Please try again.')
        return HttpResponse("Invalid report type selected. Please try again.")

def generate_pdf_report(request):
    user = request.user # Get the user object from the request
    logger.info(f'Generating a PDF report for user: {user.username}')
    print(f'Generating a PDF report for user: {user.username}') # Log the user generating the report
    
    transactions = Transaction.objects.filter(account__user=user)
    logger.info(f'User has {len(transactions)} transactions')    
    print(f'User has {len(transactions)} transactions') # Log the number of transactions

    # Predefined expense categories with associated keywords/patterns
    expense_categories = {
        'Groceries': ['grocery', 'supermarket'],
        'Dining': ['restaurant', 'cafe', 'food'],
        'Transportation': ['gas', 'fuel', 'car'],
        'Utilities': ['electricity', 'water', 'utility'],
        'Shopping': ['shopping', 'store'],
        'Other': ['subscription', 'pharmacy', 'haircut', 'salon', 'auto', 'repair'],  # Add other categories
    }
    # Preprocess transaction descriptions
    def preprocess_description(description):
        description = description.lower()
        description = re.sub(r'[^\w\s]', '', description)  # Remove punctuation
        
        for category, keywords in expense_categories.items():
            for keyword in keywords:
                if keyword in description:
                    return category
        return 'Other'  # Default category if no match found
    
    # Create a buffer to hold the PDF content
    buffer = io.BytesIO()
    print('Buffer created')
    
    # Create a PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    print('PDF document created')
    
    # Add document title
    styles = getSampleStyleSheet()
    report_title = Paragraph('Transaction Report', styles['Title'])
    elements.append(report_title)
    logger.info('Added document title')
    elements.append(Spacer(1, 24))

    # Add company data section
    company_info = [
        ('Heritage Banking'),
        ('123 Here Street'),
        ('Greenville, NC 27834'),
        ('info@xyzinc.com')
    ]
    company_data = "<br/>".join([f"<b>{value}</b>" for value in company_info])
    company_info_paragraph = Paragraph(company_data, styles['Normal'])
    elements.append(company_info_paragraph)
    logger.info('Added company data section')
    elements.append(Spacer(1, 24))
    print('Company data section added')

    # Add customer data section
    customer_info = [
        ('Customer Name:', f'{user.first_name} {user.last_name}'),
        ('Email Address:', f'{user.email}'), 
        
        
        ('Account Number:', f'{user.bank_accounts.first().account_number}'),
        ('Account Opened:', f'{user.bank_accounts.first().account_opening_date}'),
        ('Account Type:', f'{user.bank_accounts.first().account_type}'),
        
           
    ]
    customer_data = "<br/>".join([f"<b>{label}</b> {value}" for label, value in customer_info])
    customer_info_paragraph = Paragraph(customer_data, styles['Normal'])
    elements.append(customer_info_paragraph)
    logger.info('Added customer data section')
    elements.append(Spacer(1, 12))
    print('Customer data section added')
    

    # Format transaction data for inclusion in PDF
    data = [['Transaction ID', 'Type', 'Amount', 'Date', 'Description', 'Category']]
    
    
    transactions = Transaction.objects.filter(account__user=user)
    for transaction in transactions:
        category = preprocess_description(transaction.description)
        data.append([transaction.id, transaction.transaction_type, transaction.amount, transaction.timestamp, transaction.description, category])


    logger.info(f'User has {len(transactions)} transactions')
   

    print('Transaction data formatted')
    
    table = Table(data)
    table.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    elements.append(table)
    logger.info('Added transaction data section')
    print('Transaction data section added')

    # Build the PDF document
    doc.build(elements)
    logger.info('PDF report built')
    print('PDF report built')

    # Return the PDF content as a response
    buffer.seek(0)
    logger.info('Buffer set to beginning')
    return FileResponse(buffer, as_attachment=True, filename="report.pdf")

    
def generate_csv_report(request):
    user = request.user # Get the user object from the request
    logger.info(f'Generating a PDF report for user: {user.username}')
    print(f'Generating a PDF report for user: {user.username}') # Log the user generating the report
    
    transactions = Transaction.objects.filter(account__user=user)
    logger.info(f'User has {len(transactions)} transactions')    
    print(f'User has {len(transactions)} transactions') # Log the number of transactions
    
    # Predefined expense categories with associated keywords/patterns
    expense_categories = {
        'Groceries': ['grocery', 'supermarket'],
        'Dining': ['restaurant', 'cafe', 'food'],
        'Transportation': ['gas', 'fuel', 'car'],
        'Utilities': ['electricity', 'water', 'utility'],
        'Shopping': ['shopping', 'store'],
        'Other': ['subscription', 'pharmacy', 'haircut', 'salon', 'auto', 'repair'],  # Add other categories
    }
    # Preprocess transaction descriptions
    def preprocess_description(description):
        description = description.lower()
        description = re.sub(r'[^\w\s]', '', description)  # Remove punctuation
        
        for category, keywords in expense_categories.items():
            for keyword in keywords:
                if keyword in description:
                    return category
        return 'Other'  # Default category if no match found
    
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transaction_report.csv"'

    writer = csv.writer(response)

    data = [['Transaction ID', 'Type', 'Amount', 'Date', 'Description', 'Category']]
    
    # Write report title
    writer.writerow(['Transaction Report'])
    
    # Write company information
    company_info = [
        ('Company Name', 'Heritage Banking'),
        ('Address', '123 Here Street'),
        ('City', 'Greenville'),
        ('State', 'NC'),
        ('ZIP Code', '27834'),
        ('Email', 'info@xyzinc.com'),
    ]
    
    writer.writerow([])
    writer.writerow(['Company Information'])
    for item in company_info:
        writer.writerow(item)
        

    # Write customer information
    writer.writerow([])
    writer.writerow(['Customer Information'])
    customer_info = [
        ('Customer Name', f'{user.first_name} {user.last_name}'),
        ('Email Address', user.email),
        ('Account Number', user.bank_accounts.first().account_number),
        ('Account Opened', user.bank_accounts.first().account_opening_date),
        ('Account Type', user.bank_accounts.first().account_type),
    ]
    for item in customer_info:
        writer.writerow(item)


    # Write transaction data
    for transaction in transactions:
        category = preprocess_description(transaction.description)
        data.append([transaction.id, transaction.transaction_type, transaction.amount, transaction.timestamp, transaction.description, category])

    
     # Write headers
    writer.writerow([])
    writer.writerow(['Transaction ID', 'Type', 'Amount', 'Date', 'Description', 'Category'])

    # Write transaction data
    for transaction in transactions:
        category = preprocess_description(transaction.description)
        writer.writerow([
            transaction.id,
            transaction.transaction_type,
            transaction.amount,
            transaction.timestamp,
            transaction.description,
            category
        ])
    
    print('CSV report generated')
    return response




# @login_required
def wallet(request):
    user_accounts = request.user.bank_accounts.all()
    context = {'bank_accounts': user_accounts}
    return render(request, 'accounts/wallet.html', context)


def profile(request):
    # Fetch the user object from the database
    member = User.objects.get(username=request.user)

    # Pass the user object to the template
    context = {'member': member}
    return render(request, 'accounts/profile.html', context)


def register(request):
    # TODO: Add a check to see if the user is already logged in
    # TODO: VERIFY THAT THE CURRENT BELOW CODE WORKS BEFORE EDITING
    if request.method == 'POST':
        print('POST request received')
        # Get user details from the form
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        email = request.POST['email']

        print(f'\n\n\n\nUsername: {username}')
        print(f'Password: {password}')
        print(f'First Name: {first_name}')
        print(f'Last Name: {last_name}')
        print(f'Email: {email}\n\n\n')

        # Create the user object
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name

        try:
            print('Creating a new user')
            # Save the changes
            user.save()
            # log the user in
            login(request, user)
            print('User was created successfully')
            messages.success(request, 'User was created successfully')
        except Exception as e:
            print(f'An unexpected error occurred: {str(e)}')
            messages.error(request, f'An unexpected error occurred: {str(e)}')
    return render(request, 'accounts/membership.html')


def membership(request):
    if request.method == 'POST':
        print('POST request received')
        # Get user details from the form
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        email = request.POST['email']

        print(f'\n\n\n\nUsername: {username}')
        print(f'Password: {password}')
        print(f'First Name: {first_name}')
        print(f'Last Name: {last_name}')
        print(f'Email: {email}\n\n\n')

        # Create the user object
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email

        try:
            print('Creating a new user')
            # Save the changes
            user.save()
            # log the user in
            login(request, user)
            print('User was created successfully')
            messages.success(request, 'User was created successfully')
        except Exception as e:
            print(f'An unexpected error occurred: {str(e)}')
            messages.error(request, f'An unexpected error occurred: {str(e)}')

        try:
            # log the user in
            login(request, user)
            messages.success(request, 'User was created successfully')
        except Exception as e:
            print(f'An unexpected error occurred: {str(e)}')
            messages.error(request, f'An unexpected error occurred: {str(e)}')

        # User settings
        # home_address = request.POST['Address']
        # city = request.POST['City']
        # state = request.POST['State']
        # zip_code = request.POST['Zip Code']
        # country = request.POST['Country']
        profile_img_url = request.POST['profile_img_url']
        # date_of_birth = request.POST['date_of_birth']
        monthly_income = request.POST['monthly_income']
        credit_score = request.POST['credit_score']

        if profile_img_url is None:
            profile_img_url = 'https://media.istockphoto.com/id/168415745/photo/black-panther.webp?b=1&s=170667a&w=0&k=20&c=VUXE_4-AEIAJIxRvVjkbENkBfroAXrzaHlUMwE4jR_s='

        if monthly_income is None:
            monthly_income = 0

        if credit_score is None:
            credit_score = 0
        else:
            credit_score = int(credit_score)

        # Try to update user settings for the new user
        try:
            # Create a user setting and bank account for the new user
            user_settings = UserSetting.objects.get(user=user)
            user_settings.profile_img_url = profile_img_url
            # user_settings.date_of_birth = date_of_birth
            user_settings.monthly_income = monthly_income
            user_settings.credit_score = credit_score

            print(f'User profile_img_url: {user_settings.profile_img_url}')
            logger.info(f'User profile_img_url: {user_settings.profile_img_url}')
            # print(f'User date_of_birth: {user_settings.date_of_birth}')
            print(f'User monthly_income: {user_settings.monthly_income}')
            print(f'User credit_score: {user_settings.credit_score}')
            user_settings.save()
            print('User settings were created successfully')
        except Exception as e:
            print(f'An unexpected error occurred: {str(e)}')
            messages.error(request, f'An unexpected error occurred: {str(e)}')

        print('Bank account was created successfully')
        print('User was created successfully')
        messages.success(request, 'User was created successfully')
        return redirect('accounts:wallet')
    else:
        print('User was not created successfully')
        form = CustomUserCreationForm()  # An unbound form
    return render(request, 'accounts/membership.html')


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
            return redirect('accounts:dashboard')  # Redirect to the home page
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


def generate_random_9_digit_number():
    """Generates a random 9-digit numerical string."""

    random_number = get_random_string(length=9, allowed_chars='0123456789')
    return int(random_number)  # Convert to integer for numerical operations


@require_POST
def create_bank_account(request):
    # Get the user object from the
    user = User.objects.get(id=request.user.id)
    account_type = request.POST.get('account_type')
    deposit_amount = request.POST.get('deposit_amount')

    if account_type is None:
        account_type = 'Savings'

    if deposit_amount is None:
        deposit_amount = 0
    else:
        deposit_amount = Decimal(deposit_amount)

    try:
        # Create a new bank account
        print('Creating a new bank account')
        new_account = BankAccount.objects.create(
            user=user,
            account_number=generate_unique_account_number(),
            account_type=account_type,
            balance=deposit_amount
        )
        new_account.save()
        print('Bank account was created successfully')
        logger.info('Bank account was created successfully')
        messages.success(request, 'Bank account was created successfully')
        return redirect('accounts:wallet')
    except Exception as e:
        print(f'An unexpected error occurred: {str(e)}')
        logger.error(f'An unexpected error occurred: {str(e)}')
        messages.error(request, f'An unexpected error occurred: {str(e)}')
        return redirect('accounts:wallet')


# TODO: Rename the function to create_bank_transaction
@login_required  # Require users to be logged in
def create_bank_transaction(request):
    if request.method != 'POST':
        return redirect('accounts:dashboard')  # Redirect if not a POST request

    # Input Sanitization & Validation
    account_from_number = request.POST.get('account_from_number')
    account_to_number = request.POST.get('account_to_number')
    amount = request.POST.get('amount')
    transaction_type = request.POST.get('transaction_type')
    description = request.POST.get('description')

    print(f'Account from: {account_from_number}')
    print(f'Account to: {account_to_number}')
    print(f'Amount: {amount}')
    print(f'Transaction type: {transaction_type}')
    print(f'Description: {description}')

    # Validate required input fields
    if not all([amount, transaction_type]):
        print('All fields (amount, type, description) are required.')
        messages.error(request, 'All fields (amount, type, description) are required.')
        return render(request, 'accounts/dashboard.html')

    try:
        amount = Decimal(amount)
        if amount <= 0:
            raise ValueError('Amount must be greater than zero.')
    except (ValueError, Decimal.InvalidOperation):
        print('Please enter a valid amount.')
        messages.error(request, 'Please enter a valid amount.')
        return render(request, 'accounts/dashboard.html')

    if transaction_type not in ('deposit', 'withdrawal', 'transfer', 'payment'):
        print('Invalid transaction type.')
        messages.error(request, 'Invalid transaction type.')
        return render(request, 'accounts/dashboard.html')

    # User and Account Existence Check
    try:
        account = request.user.bank_accounts.all().first()
        if not account:
            print()
            raise ObjectDoesNotExist('User has no linked bank account.')
    except ObjectDoesNotExist as e:
        print(f'User has no linked bank account: {e}')
        logger.warning(str(e))
        messages.error(request, 'No linked bank account found.')
        return render(request, 'accounts/dashboard.html')

    # Account Number Handling
    def handle_account_number(account_number):
        if account_number:
            try:
                print(f'Account number: {account_number}')
                return BankAccount.objects.get(account_number=account_number)
            except ObjectDoesNotExist:
                print(f'Account number {account_number} does not exist.')
                messages.error(request, f'Account number {account_number} does not exist.')
                return None
        else:
            print('Account number is required.')
            messages.error(request, 'Account number is required.')
            return None

    account_from = handle_account_number(account_from_number)
    account_to = handle_account_number(account_to_number)

    if not account_from or not account_to:
        print('Invalid account number(s).')
        return render(request, 'accounts/dashboard.html')

    # Duplicate Transaction Prevention (Simplified)
    if Transaction.objects.filter(
        account=account,
        transaction_type=transaction_type,
        amount=amount,
        description=description,
        # Add date comparison if needed
    ).exists():
        print('A similar transaction already exists.')
        messages.warning(request, 'A similar transaction already exists.')
        return render(request, 'accounts/dashboard.html')

    # Transaction Logic (with error handling within try-except)
    try:
        new_transaction = Transaction(
            account=account,  # Determine correct account based on type
            transaction_type=transaction_type,
            amount=amount,
            description=description
        )
        new_transaction.full_clean()

        if transaction_type == 'deposit':
            account.balance += amount

        elif transaction_type == 'withdrawal':
            if account.balance < amount:
                raise ValueError('Insufficient funds for withdrawal.')
            account.balance -= amount

        elif transaction_type == 'transfer':
            if account_from.balance < amount:
                raise ValueError('Insufficient funds for transfer.')
            account_from.balance -= amount
            account_to.balance += amount

            new_transaction_to = Transaction(
                account=account_to,  # Determine correct account based on type
                transaction_type=transaction_type,
                amount=amount,
                description='Transfer from ' + account_from_number
            )
            new_transaction.description = 'Transfer to ' + account_to_number
            new_transaction.account.balance = float(new_transaction.account.balance) - float(amount)
            new_transaction_to.account.balance = float(new_transaction_to.account.balance) + float(amount)
            new_transaction.full_clean()
            # Create second transaction for clarity

        # Save changes
        new_transaction.save()
        if transaction_type == 'transfer' and new_transaction_to:
            new_transaction_to.save()
        account.save()  # Save changes to account balance
        if transaction_type == 'transfer':
            account_to.save()

        messages.success(request, 'Transaction successful!')
        return redirect('accounts:wallet')  # Redirect to success page

    except ValueError as e:
        logger.error(f'Transaction failed: {e}')
        print(f'\n\nTransaction failed: {e}')
        messages.error(request, str(e))
    except Exception as e:
        logger.exception(f'Unexpected error during transaction: {e}')
        print(f'\n\nUnexpected error during transaction: {e}')
        messages.error(request, 'An unexpected error occurred.')

    return render(request, 'accounts/dashboard.html')


# Create an 'Account' profile automatically when registering new user***
logger = logging.getLogger(__name__)

PROFILE_IMAGE_URL = 'https://images.unsplash.com/photo-1710488140458-e1757928a9f8?q=80&w=1740&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
STARTING_BALANCE = 200.00
ACCOUNT_TYPE = 'Checking'


def create_profile(sender, instance, created, **kwargs):
    if created:
        try:
            # Create a user setting and bank account for the new user
            user_settings = UserSetting.objects.create(
                user=instance,
                profile_img_url=PROFILE_IMAGE_URL,
            )
            logger.info('User settings were created successfully')
        except Exception as e:
            print(f'An unexpected error occurred: {str(e)}')
            error_message = f'An error occurred while creating user settings: {str(e)}'
            logger.error(error_message)
            messages.error(error_message)

        try:
            # Create a bank account for the new user
            print('Creating a bank account for the new user')
            bank_account = BankAccount.objects.create(
                user=instance,
                account_number=generate_unique_account_number(),
                account_type=ACCOUNT_TYPE,
                balance=STARTING_BALANCE
            )
            bank_account.save()

            # Create an initial deposit transaction for the new bank account
            print('Creating an initial deposit transaction for the new bank account')
            transaction = Transaction.objects.create(
                account=bank_account,
                transaction_type='deposit',
                amount=STARTING_BALANCE,
                description='Initial deposit',
                timestamp=datetime.now()
            )
            print(datetime.now())
            print('Initial deposit transaction was created successfully')
            transaction.save()

            logger.info('Bank account was created successfully')
            logger.info(f'Bank account number: {bank_account.account_number}')
            logger.info(f'Bank account type: {bank_account.account_type}')
            logger.info(f'Bank account balance: {bank_account.balance}')
        except Exception as e:
            print(f'An unexpected error occurred: {str(e)}')
            error_message = f'An error occurred while creating a bank account: {str(e)}'
            logger.error(error_message)
            messages.error(error_message)


post_save.connect(create_profile, sender=User)


def update_settings(user_id, credit_score=None, monthly_income=None):
    # user = User.objects.get(id=user_id)
    user_settings = UserSetting.objects.get(id=user_id)
    try:
        if monthly_income is not None:
            user_settings.monthly_income = monthly_income
        if credit_score is not None:
            user_settings.credit_score = credit_score

        user_settings.save()
    except Exception as e:
        print(f'An unexpected error occurred: {str(e)}')
        error_message = f'An error occurred while updating user settings: {str(e)}'
        logger.error(error_message)
        messages.error(error_message)

    # def update_credit_score(request):
    #     user_id = request.user.id
    #     credit_score = request.POST.get('credit_score')
    #     update_settings(user_id, credit_score=credit_score)
    #     return render(request, 'accounts/settings.html')

# def update_spending_limit(request):
#     if request.method == 'POST':
#         form = SpendingLimitForm(request.user, request.POST)
#         if form.is_valid():
#             account = form.cleaned_data['account']
#             account.spending_limit = form.cleaned_data['spending_limit']
#             account.save()
#             return redirect('dashboard')
#     else:
#         form = SpendingLimitForm(request.user)
#     return render(request, 'dashboard.html', {'form': form})