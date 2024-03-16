from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views import generic
from psycopg2 import IntegrityError

from .forms import CustomUserCreationForm, generate_unique_account_number
from django.contrib import messages  # for messages
from django.contrib.auth import authenticate, logout, login

from .models import Transaction, BankAccount, UserSetting
from django.utils.crypto import get_random_string


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
    user_settings = UserSetting.objects.get(user=request.user)
    context = {'user_settings': user_settings}
    monthly_income = context['user_settings'].monthly_income
    annual_income = monthly_income * 12
    return render(request, 'accounts/dashboard.html', {'monthly_income': monthly_income, 'annual_income': annual_income})

# def dashboard(request):
#     monthly_income = 2000
#     annual_income = monthly_income * 12
#     member = request.user
#     return render(request, 'accounts/dashboard.html', {'member': member, 'monthly_income': monthly_income, 'annual_income': annual_income})



def generate_report(request):
    member = request.user
    context = {'member': member}
    return render(request, 'accounts/reports.html', {'member': member})







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
        initial_deposit = request.POST['deposit_amount']
        account_type = request.POST['account_type']

        if profile_img_url is None:
            profile_img_url = 'https://media.istockphoto.com/id/168415745/photo/black-panther.webp?b=1&s=170667a&w=0&k=20&c=VUXE_4-AEIAJIxRvVjkbENkBfroAXrzaHlUMwE4jR_s='

        # Bank-Account Initial Transaction/Deposit
        if account_type is None:
            account_type = 'Checking'
        elif account_type == 'Checking':
            account_type = 'Checking'
        elif account_type == 'Savings':
            account_type = 'Savings'

        if initial_deposit is None:
            initial_deposit = 200.00

        if monthly_income is None:
            monthly_income = 4200.00

        try:
            # Create a user setting and bank account for the new user
            user_settings = UserSetting.objects.create(
                user=user,
                profile_img_url=profile_img_url,
                # date_of_birth=date_of_birth,
                monthly_income=monthly_income,
                credit_score=credit_score
            )
            print(f'User profile_img_url: {user_settings.profile_img_url}')
            # print(f'User date_of_birth: {user_settings.date_of_birth}')
            print(f'User monthly_income: {user_settings.monthly_income}')
            print(f'User credit_score: {user_settings.credit_score}')
            user_settings.save()
            print('User settings were created successfully')
        except Exception as e:
            print(f'An unexpected error occurred: {str(e)}')
            messages.error(request, f'An unexpected error occurred: {str(e)}')

        try:
            print('Creating a new bank account')
            # Create a bank account for the new user
            bank_account = BankAccount.objects.create(
                user=user,
                account_number=generate_unique_account_number(),
                account_type=account_type,
                balance=initial_deposit
            )
            bank_account.save()
            print(f'Bank account number: {bank_account.account_number}')
            print(f'Bank account type: {bank_account.account_type}')
            print(f'Bank account balance: {bank_account.balance}')
            print('Bank account was created successfully')
        except Exception as e:
            print(f'An unexpected error occurred: {str(e)}')
            messages.error(request, f'An unexpected error occurred: {str(e)}')

        try:
            print('Creating a new transaction')
            # Create a transaction for the initial deposit
            transaction = Transaction.objects.create(
                account=bank_account,
                transaction_type='deposit',
                amount=initial_deposit,
                description='Initial Deposit'
            )
            transaction.save()
            print(f'Transaction type: {transaction.transaction_type}')
            print(f'Transaction amount: {transaction.amount}')
            print(f'Transaction description: {transaction.description}')
            print('Initial deposit transaction was created successfully')
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


def generate_random_9_digit_number():
    """Generates a random 9-digit numerical string."""

    random_number = get_random_string(length=9, allowed_chars='0123456789')
    return int(random_number)  # Convert to integer for numerical operations


def create_deposit_transaction(request):
    # Fetch the user object from the database
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    amount = request.POST.get('amount')
    print(f'Amount: {amount}')
    account_id = request.POST.get('account_id')
    if account_id is None:
        print('Account ID is None')
        account_id = generate_random_9_digit_number()
        print(f'After None -> Account ID: {account_id}')

    transaction_type = request.POST.get('transaction_type')
    print(f'Transaction Type: {transaction_type}')
    description = request.POST.get('description')
    print(f'Description: {description}')

    if transaction_type is None:
        transaction_type = 'deposit'
    elif transaction_type == 'deposit':
        transaction_type = 'deposit'
    elif transaction_type == 'withdrawal':
        transaction_type = 'withdrawal'

    # Validate input data

    # if not all([user_id, amount]):
    #     print()
    #     print()
    #     print(f'User ID: {user_id}')
    #     print(f'Amount: {amount}')
    #     print()
    #     print()
    #     print('Values are unvalid')
    #     messages.error(request, 'Please fill in all required fields.')
    #     return render(request, 'dash/dashboard.html')  # Consider using an error template

    # Create a new transaction object
    try:
        print('Creating a new transaction')
        new_transaction = Transaction(account=user.bank_accounts.all.first, transaction_type=transaction_type, amount=amount,
                                      description=description)
        new_transaction.save()
        print('Deposit successful!')
        messages.success(request, 'Deposit successful!')
        return render(request, 'accounts/wallet.html')  # Success template
    except IntegrityError:
        print('An error occurred during transaction creation.')
        messages.error(request, 'An error occurred during transaction creation.')
    except Exception as e:  # Catch other potential exceptions
        print(f'An unexpected error occurred: {str(e)}')
        messages.error(request, f'An unexpected error occurred: {str(e)}')

    return render(request, 'dash/dashboard.html')  # Re-render form on error
