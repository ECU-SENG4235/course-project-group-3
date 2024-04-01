from django.urls import path, include

from .views import SignUpView

from accounts import views

app_name = 'accounts'  # ensure this line is here, the value should match the namespace you used in the main urls.py

urlpatterns = [
    path('', views.wallet, name='wallet'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('settings/', views.settings, name='settings'),

<<<<<<< Updated upstream
=======
    # Transaction URLs
    path('create_deposit_transaction/', views.create_bank_transaction, name='create_bank_transaction'),
    path('create_new_account/', views.membership, name='membership'),

    # Account URLs
    path('create_bank_account/', views.create_bank_account, name='create_bank_account'),

#     TODO: Add URL to generate report (Curtis)
    path('generate_report/', views.generate_report, name='generate_report'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),
    path('generate_csv/', views.generate_csv, name='generate_csv'),
>>>>>>> Stashed changes
]
