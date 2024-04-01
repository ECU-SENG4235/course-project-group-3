import random
import string
from urllib import request

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from accounts.models import UserSetting, BankAccount


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


def generate_unique_account_number():
    digits = string.digits  # String containing digits (0-9)
    account_number = ''.join(random.choice(digits) for _ in range(8))
    while BankAccount.objects.filter(account_number=account_number).exists():
        account_number = ''.join(random.choice(digits) for _ in range(8))
    return int(account_number)


# def create_user(self, username, email, password, **extra_fields):
#     user = super().create_user(username, email, password, **extra_fields)
#     # Create a user setting and bank account for the new user
#     settings = UserSetting.objects.create(user=user)
#     settings.save()
#     account = BankAccount.objects.create(account_number=generate_unique_account_number())
#     account.save()
#
#     return user

class SpendingLimitForm(forms.Form):
    account = forms.ModelChoiceField(queryset=BankAccount.objects.all())
    spending_limit = forms.DecimalField(max_digits=10, decimal_places=2)

    def __init__(self, user, *args, **kwargs):
        super(SpendingLimitForm, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = BankAccount.objects.filter(user=user)