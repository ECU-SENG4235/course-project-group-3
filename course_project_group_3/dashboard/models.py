from django.db import models

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    address = models.TextField()
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email_address = models.CharField(max_length=255, null=True, blank=True)
    # Additional user profile information can be added here

    class Meta:
        db_table = 'user_profile'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profile'

    def __str__(self):
        return f"{self.user.username}'s Profile"

class UserSettings(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    theme = models.CharField(max_length=100, default='light')
    language = models.CharField(max_length=100, default='en')
    is_notifications_enabled = models.BooleanField(default=True)
    font_size = models.IntegerField(default=12)

    # TODO:  ST-2/ST-3  Add more settings attributes here!!!
    timezone = models.CharField(max_length=50, default='UTC')
    preferred_currency = models.CharField(max_length=3, default='USD')
    email_notifications = models.BooleanField(default=True)
    dark_mode_start_time = models.TimeField(null=True, blank=True)
    dark_mode_end_time = models.TimeField(null=True, blank=True)
    show_balance_on_dashboard = models.BooleanField(default=True)
    # Add more user settings attributes here!!!

    class Meta:
        db_table = 'user_settings'
        verbose_name = 'User Setting'
        verbose_name_plural = 'User Settings'

    def __str__(self):
        return f"{self.user.username}'s User Settings"


class Account(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    account_type = models.CharField(max_length=50, choices=[('savings', 'Savings'), ('checking', 'Checking')], default='checking')
    is_account_active = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    transaction_limit = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)
    overdraft_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    account_type = models.CharField(max_length=50, choices=[('savings', 'Savings'), ('checking', 'Checking')], default='checking')
    last_transaction_date = models.DateTimeField(null=True, blank=True)

    # Additional Banking Attributes
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    monthly_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    withdrawal_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    minimum_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    account_opening_date = models.DateField()
    account_closure_date = models.DateField(null=True, blank=True)
    is_joint_account = models.BooleanField(default=False)
    joint_account_users = models.ManyToManyField('auth.User', related_name='joint_accounts', blank=True)
       
    # TODO: ST-2/ST-3  Add more settings attributes here!!!

    class Meta:
        db_table = 'accounts'
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    def __str__(self):
        return f"{self.user.username}'s {self.account_type} Account"

class Transactions(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
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
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
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
