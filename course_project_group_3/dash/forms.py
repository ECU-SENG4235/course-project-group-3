from django import forms

from course_project_group_3.dash.models import UserSetting


# Create a User Settings form, to be used in Django,for user profile customization
class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = UserSetting
        fields = ['theme', 'language', 'is_notifications_enabled', 'font_size', 'timezone', 'preferred_currency',
                  'email_notifications', 'dark_mode_start_time', 'dark_mode_end_time', 'show_balance_on_dashboard']
        labels = {
            'theme': 'Theme',
            'language': 'Language',
            'is_notifications_enabled': 'Notifications',
            'font_size': 'Font Size',
            'timezone': 'Timezone',
            'preferred_currency': 'Preferred Currency',
            'email_notifications': 'Email Notifications',
            'dark_mode_start_time': 'Dark Mode Start Time',
            'dark_mode_end_time': 'Dark Mode End Time',
            'show_balance_on_dashboard': 'Show Balance on Dashboard',
        }
        widgets = {
            'theme': forms.Select(attrs={'class': 'form-control'}),
            'language': forms.Select(attrs={'class': 'form-control'}),
            'is_notifications_enabled': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'font_size': forms.NumberInput(attrs={'class': 'form-control'}),
            'timezone': forms.Select(attrs={'class': 'form-control'}),
            'preferred_currency': forms.Select(attrs={'class': 'form-control'}),
            'email_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'dark_mode_start_time': forms.TimeInput(attrs={'class': 'form-control'}),
            'dark_mode_end_time': forms.TimeInput(attrs={'class': 'form-control'}),
            'show_balance_on_dashboard': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
