from django.shortcuts import render, redirect
from .models import UserProfile, Account, Transaction, UserSettings, CreditCard
from .forms import UserSettingsForm

def user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return render(request, 'error.html', {'error_message': 'User profile not found.'})

    context = {
        'user_profile': user_profile,
    }

    return render(request, 'dashboard/user_profile.html', context)

def user_settings(request):
    try:
        user_settings = UserSettings.objects.get(user=request.user)
    except UserSettings.DoesNotExist:
        return render(request, 'error.html', {'error_message': 'User settings not found.'})

    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=user_settings)
        if form.is_valid():
            form.save()
            return redirect('user_settings')
    else:
        form = UserSettingsForm(instance=user_settings)

    context = {
        'user_settings': user_settings,
        'form': form,
    }

    return render(request, 'dashboard/user_settings.html', context)

def account_details(request, account_id):
    try:
        user_account = Account.objects.get(id=account_id, user=request.user)
    except Account.DoesNotExist:
        return render(request, 'error.html', {'error_message': 'Account not found.'})

    recent_transactions = Transaction.objects.filter(account=user_account).order_by('-timestamp')[:10]

    context = {
        'user_account': user_account,
        'recent_transactions': recent_transactions,
    }
    return render(request, 'dashboard/account_details.html', context)

def recent_transactions(request, account_id):
    try:
        user_account = Account.objects.get(id=account_id, user=request.user)
    except Account.DoesNotExist:
        return render(request, 'error.html', {'error_message': 'Account not found.'})

    recent_transactions = Transaction.objects.filter(account=user_account).order_by('-timestamp')[:10]

    context = {
        'user_account': user_account,
        'recent_transactions': recent_transactions,
    }

    return render(request, 'dashboard/recent_transactions.html', context)

def credit_card_details(request):
    try:
        user_credit_card = CreditCard.objects.get(account__user=request.user)
    except CreditCard.DoesNotExist:
        return render(request, 'error.html', {'error_message': 'Credit card details not found.'})

    context = {
        'user_credit_card': user_credit_card,
    }

    return render(request, 'credit_cards/credit_card_details.html', context)