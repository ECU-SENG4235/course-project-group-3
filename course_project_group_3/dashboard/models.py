from django.db import models

# Create your models here.


class UserSettings(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    theme = models.CharField(max_length=100, default='light')
    language = models.CharField(max_length=100, default='en')
    # TODO:  ST-2/ST-3  Add more settings attributes here!!!

    class Meta:
        db_table = 'user_settings'
        verbose_name = 'User Setting'
        verbose_name_plural = 'User Settings'

    def __str__(self):
        return self.user.username


class Account(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # TODO: ST-2/ST-3  Add more settings attributes here!!!

    class Meta:
        db_table = 'accounts'
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    def __str__(self):
        return self.user.username
