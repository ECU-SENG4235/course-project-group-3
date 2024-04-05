from django.contrib.auth.models import User
from django.db.models.signals import post_save

from .models import UserSetting, BankAccount  # Assuming models are in the same app


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserSetting.objects.create(user=instance)
        BankAccount.objects.create(user=instance, account_type='checking')  # Set a default account type


post_save.connect(create_user_profile, sender=User)
