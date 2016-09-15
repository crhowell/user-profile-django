from django.contrib.auth.models import User
from django import forms


def pwd_is_same(old, new):
    if old == new:
        raise forms.ValidationError(
            'Your new password cannot be the same as your old password.')


def min_length(new, length):
    if not len(new) > length:
        raise forms.ValidationError(
            'Your password must be at least {} characters'.format(length))


def contains_num(new):
    if not any(c.isdigit() for c in new):
        raise forms.ValidationError(
            'Your password must contain at least 1 number.')


def contains_upper(new):
    if not any(c.isupper() for c in new):
        raise forms.ValidationError(
            'Your password must contain at least 1 uppercase character.')


def contains_lower(new):
    if not any(c.islower() for c in new):
        raise forms.ValidationError(
            'Your password must contain at least 1 lowercase character.')


def contains_special(new):
    specials = ['!', '@', '#', '^', '&', '*']
    if not any(True for c in new if c in specials):
        raise forms.ValidationError(
            'Your password must contain at least 1 special character.')


def pwd_contains(string, new, msg=''):
    if string:
        message = msg if msg else 'cannot contain {}'.format(string)
        pwd = new.lower()
        if not pwd.find(string.lower()) == -1:
            raise forms.ValidationError('Your password '+message)


def validate_all(user, old, new, length=14):
    min_length(new, length=8)  # Check password is GT length
    pwd_is_same(old, new)  # Check old is same as new password
    contains_num(new)  # Check password for number
    contains_upper(new)  # Check password for uppercase
    contains_lower(new)  # Check password for lowercase
    contains_special(new)  # Check password for special character

    # Check password contains registered username
    pwd_contains(user.username, new, 'cannot contain your username')
    # Check password contains First Name
    pwd_contains(
        user.user_profile.first_name, new, 'cannot contain your first name')
    # Check password contains Last Name
    pwd_contains(
        user.user_profile.last_name, new, 'cannot contain your last name')


class ChangePasswordForm(forms.ModelForm):
    old_password = forms.CharField(required=True,
                                   label='Old password',
                                   widget=forms.PasswordInput)
    password1 = forms.CharField(required=True,
                                label='New password',
                                widget=forms.PasswordInput)
    password2 = forms.CharField(required=True,
                                label='Verify new password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['old_password', 'password1', 'password2']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')

        if not self.user.check_password(old_password):
            raise forms.ValidationError('Your old password does not match.')
        return old_password

    def clean_password2(self):
        old_password = self.cleaned_data.get('old_password')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 == password2:
            # Validate field against all checks
            validate_all(self.user, old_password, password2, length=14)
            return password2
        else:
            raise forms.ValidationError(
                'Your NEW passwords do not match.'
            )

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['password1'])
        if commit:
            self.user.save()
        return self.user
