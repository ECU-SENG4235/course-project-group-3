from django.contrib import admin

from .models import BankAccount, UserSetting, CreditCard, Transaction

# Register your models here.
admin.site.register(BankAccount)
admin.site.register(UserSetting)
admin.site.register(CreditCard)
admin.site.register(Transaction)
