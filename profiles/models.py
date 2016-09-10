from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile')
    first_name = models.CharField(max_length=100, blank=True, default='')
    last_name = models.CharField(max_length=100, blank=True, default='')
    profile_uid = models.CharField(max_length=50, unique=True)
    email = models.EmailField(blank=True, default='')
    dob = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True, default='')
    avatar = models.ImageField('Profile avatar',
                               upload_to='avatars/',
                               null=True,
                               blank=True)
    has_setup = models.BooleanField(default=False)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @classmethod
    def create_profile(cls, user=None):
        if user is not None:
            try:
                cls.objects.create(user=user)
            except ValueError:
                print('Could not create profile.')
