from datetime import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.crypto import get_random_string


# Create your models here.

class UserSetting(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    theme = models.CharField(max_length=100, default='light')
    language = models.CharField(max_length=100, default='en')
    is_notifications_enabled = models.BooleanField(default=True)
    font_size = models.IntegerField(default=12)
    profile_img_url = models.URLField(null=True, blank=True)

    timezone = models.CharField(max_length=50, default='UTC')
    preferred_currency = models.CharField(max_length=3, default='USD')
    email_notifications = models.BooleanField(default=True)
    dark_mode_start_time = models.TimeField(null=True, blank=True)
    dark_mode_end_time = models.TimeField(null=True, blank=True)
    show_balance_on_dashboard = models.BooleanField(default=True)

    monthly_income = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    # monthly_expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    # monthly_savings = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    # monthly_debt = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    # monthly_investments = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    # monthly_retirement = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    credit_score = models.IntegerField(default=0)
    # credit_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    # credit_utilization = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    # credit_card_debt = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    # credit_card_interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    phone_number = models.CharField(max_length=15, null=True, blank=True)

    class Meta:
        db_table = 'user_settings'
        verbose_name = 'User Setting'
        verbose_name_plural = 'User Settings'

    def __str__(self):
        return f"{self.user.username}'s User Settings"


ACCOUNT_TYPE_CHOICES = [
    ('savings', 'Savings'),
    ('checking', 'Checking'),
    ('credit', 'Credit'),
    ('loan', 'Loan'),
    ('investment', 'Investment'),
    ('retirement', 'Retirement'),
    ('other', 'Other'),
]


class BankAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bank_accounts')
    account_number = models.PositiveIntegerField(unique=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    account_type = models.CharField(max_length=50, choices=ACCOUNT_TYPE_CHOICES, default='checking')
    is_active = models.BooleanField(default=True)

    transaction_limit = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)
    overdraft_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    last_transaction_date = models.DateTimeField(null=True, blank=True)

    # Additional Banking Attributes
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    monthly_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    withdrawal_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    minimum_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    account_opening_date = models.DateField(default=datetime.now)
    account_closure_date = models.DateField(null=True, blank=True)

    is_joint_account = models.BooleanField(default=False)

    # joint_account_users = models.ManyToManyField('User', related_name='joint_accounts', blank=True)

    # def save(self, *args, **kwargs):
    #     if self.pk is None:  # Check if it's a new object
    #         self.account_number = _generate_unique_account_number()
    #     super().save(*args, **kwargs)  # Call the original save method

    def clean(self):
        if self.balance < 0:
            raise ValidationError('Balance cannot be negative.')

    def __str__(self):
        return f"{self.user}'s {self.account_type} Account"


class Transaction(models.Model):
    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=50, choices=[('deposit', 'Deposit'), ('withdrawal', 'Withdrawal')])
    transaction_limit = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    # Additional transaction-related attributes can be added here.

    class Meta:
        db_table = 'transactions'
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    def __str__(self):
        return f"{self.account.user.username}'s Transactions"


class CreditCard(models.Model):
    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='credit_cards')
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2)
    available_credit = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField(null=True, blank=True)
    reward_points = models.IntegerField(default=0)

    # Additional credit card-related attributes can be added here.

    class Meta:
        db_table = 'credit_cards'
        verbose_name = 'Credit Card'
        verbose_name_plural = 'Credit Cards'

    def __str__(self):
        return f"{self.account.user.username}'s Credit Cards"
