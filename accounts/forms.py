from django.contrib.auth.models import User
from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email',
                  'date_of_birth', 'short_bio', 'avatar']


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='Old password')
    new_password = forms.CharField(label='New password')
    verify_password = forms.CharField(label='Verify new password')
