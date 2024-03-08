"""
URL configuration for course_project_group_3 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from dash import views

# from django.contrib.auth.decorators import login_required

app_name = 'dash'  # ensure this line is here, the value should match the namespace you used in the main urls.py


urlpatterns = [
    path('', views.index, name='dashboard'),  # django will match this to 'dash:dashboard'

]

# # Users URLs
# path('profile/', views.user_profile, name='user_profile'),
# path('settings/', views.user_settings, name='user_settings'),
#
# # Accounts URLs
# path('account/<int:account_id>/', views.account_details, name='account_details'),
#
# # Transactions URLs
# path('recent-transactions/<int:account_id>/', views.recent_transactions, name='recent_transactions'),
#
# # Credit Cards URLs
# path('credit-card-details/', views.credit_card_details, name='credit_card_details'),
