from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='user')
    first_name = models.CharField(max_length=100, blank=True, default='')
    last_name = models.CharField(max_length=100, blank=True, default='')
    email = models.EmailField(blank=True, default='')
    date_of_birth = models.DateField(null=True, blank=True, default=datetime.today)
    short_bio = models.TextField(blank=True, default='')
    avatar = models.ImageField(upload_to='avatars', blank=True, default='')

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @classmethod
    def create_profile(cls, user=None):
        if user is not None:
            try:
                cls.objects.create(user=user)
            except ValueError:
                print('Could not create profile.')
