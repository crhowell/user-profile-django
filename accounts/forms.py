from django.contrib.auth.models import User
from django import forms


class ChangePasswordForm(forms.ModelForm):
    old_password = forms.CharField(label='Old password', widget=forms.PasswordInput)
    password1 = forms.CharField(label='New password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Verify new password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = []

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')

        if not self.user.check_password(old_password):
            raise forms.ValidationError('Your old password does not match.')
        return old_password

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2:
            if password1 == password2:
                return password2
            else:
                raise forms.ValidationError('Sorry, your passwords do not match.')

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['password1'])
        if commit:
            self.user.save()
        return self.user
