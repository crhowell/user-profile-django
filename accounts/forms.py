from django import forms


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='Old password')
    new_password = forms.CharField(label='New password')
    verify_password = forms.CharField(label='Verify new password')
