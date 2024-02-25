from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserSettings, Account, Transaction, CreditCard, Payee

class ModelTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create test data for models
        self.user_profile = UserProfile.objects.create(user=self.user, full_name='Test User', email='testuser@example.com')
        self.user_settings = UserSettings.objects.create(user=self.user, theme='light', language='en')
        self.account = Account.objects.create(user=self.user, balance=1000.0, account_type='checking', is_active=True)
        self.transaction = Transaction.objects.create(account=self.account, transaction_type='deposit', amount=500.0)
        self.credit_card = CreditCard.objects.create(account=self.account, credit_limit=2000.0, available_credit=1500.0)

    def test_user_profile_model(self):
        self.assertEqual(str(self.user_profile), f"{self.user.username}'s Profile")

    def test_user_settings_model(self):

        self.assertEqual(str(self.user_settings), self.user.username)

    def test_account_model(self):
        self.assertEqual(str(self.account), f"{self.user.username}'s checking Account")

    def test_transaction_model(self):
        self.assertEqual(str(self.transaction), f"Transaction of {self.transaction.amount} in {self.transaction.account}")

    def test_credit_card_model(self):
        self.assertEqual(str(self.credit_card), f"{self.user.username}'s Credit Card")

class ViewTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_index_view(self):
        client = Client()
        client.force_login(self.user)
        response = client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/index.html')
        # Add more assertions based on your view behavior

    def test_user_profile_view(self):
        client = Client()
        client.force_login(self.user)
        response = client.get(reverse('user_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_profile.html')

    def test_user_settings_view(self):
        client = Client()
        client.force_login(self.user)
        response = client.get(reverse('user_settings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_settings.html')

    def test_account_details_view(self):
        client = Client()
        client.force_login(self.user)
        response = client.get(reverse('account_details', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/account_details.html')

    def recent_transactions_view(self):
        client = Client()
        client.force_login(self.user)
        response = client.get(reverse('recent_transactions'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transactions/recent_transactions.html')

    def credit_card_details_view(self):
        client = Client()
        client.force_login(self.user)
        response = client.get(reverse('credit_card_details'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'credit_cards/credit_card_details.html')
        # Add more assertions based on your view behavior

    # Add more view tests as needed
