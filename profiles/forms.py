from django.contrib.auth.models import User
from django import forms
from django.core import validators

from .models import Profile


def valid_bio(bio='', length=5):
    if not len(bio) > length:
        raise forms.ValidationError(
            'Your bio must be more than {} characters'.format(length))


class ProfileForm(forms.ModelForm):
    verify_email = forms.EmailField()

    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'email',
            'verify_email',
            'dob',
            'profile_uid',
            'avatar',
            'bio'
        ]

    def clean_verify_email(self):
        email = self.cleaned_data.get('email').lower()
        verify_email = self.cleaned_data.get('verify_email').lower()
        if email != verify_email:
            raise forms.ValidationError('Email fields do not match.')
        return email

    def clean_bio(self):
        bio = self.cleaned_data.get('bio')
        valid_bio(bio, 10)
        return bio


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'email',
            'dob',
            'avatar',
            'bio'
        ]

    def clean_bio(self):
        bio = self.cleaned_data.get('bio')
        valid_bio(bio, 10)
