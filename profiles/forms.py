from django.contrib.auth.models import User
from django import forms
from django.core import validators

from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'email',
            'dob',
            'profile_uid',
            'avatar',
            'bio'
        ]
