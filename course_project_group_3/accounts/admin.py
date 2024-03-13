from django.contrib import admin

from .models import Account, UserSetting, CreditCard, Transaction


# Register your models here.
admin.site.register(Account)
admin.site.register(UserSetting)
admin.site.register(CreditCard)
admin.site.register(Transaction)
