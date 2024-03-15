from django.urls import path, include

from .views import SignUpView

from accounts import views

app_name = 'accounts'  # ensure this line is here, the value should match the namespace you used in the main urls.py

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('accounts/', views.wallet, name='wallet'),
    path('login/', views.login_user, name='login_user'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.membership, name='register'),
    path('settings/', views.settings, name='settings'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),  # django will match this to 'dash:dashboard'

    # Transaction URLs
    path('create_deposit_transaction/', views.create_deposit_transaction, name='create_deposit_transaction'),
    path('create_new_account/', views.membership, name='membership'),

#     TODO: Add URL to generate report (Curtis)
    path('generate_report/', views.generate_report, name='generate_report'),
]
