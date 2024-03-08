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

]
