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
from users import views as user_views
from accounts import views as account_views
from transactions import views as transaction_views
from credit_cards import views as credit_card_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),

    # Users URLs
    path('user-profile/', login_required(user_views.user_profile), name='user_profile'),
    path('user-settings/', login_required(user_views.user_settings), name='user_settings'),

    # Accounts URLs
    path('account/<int:account_id>/', login_required(account_views.account_details), name='account_details'),

    # Transactions URLs
    path('recent-transactions/<int:account_id>/', login_required(transaction_views.recent_transactions), name='recent_transactions'),

    # Credit Cards URLs
    path('credit-card-details/', login_required(credit_card_views.credit_card_details), name='credit_card_details'),

    # Add more URLs as needed    # Include the URLs from the dashboard app
    path('dashboard/', include('dashboard.urls')),
]
