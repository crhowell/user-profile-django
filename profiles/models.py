import hashlib
import os

from django.contrib.auth.models import User
from django.db import models


# Gravatar Alternative
def alt_avatar_url(email):
    m = hashlib.md5()
    m.update(email.encode('utf-8'))
    return 'https://www.gravatar.com/avatar/{}?d=identicon'.format(m.hexdigest())


def image_upload(instance, filename):
    print(instance)
    if filename:
        base_filename, filename_ext = os.path.splitext(filename)
        return 'avatars/{}/{}{}'.format(
            instance.profile_uid,
            base_filename.lower(),
            filename_ext.lower()
        )


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile')
    first_name = models.CharField(max_length=100, blank=True, default='')
    last_name = models.CharField(max_length=100, blank=True, default='')
    profile_uid = models.CharField(max_length=50, unique=True)
    email = models.EmailField(blank=True, default='')
    dob = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True, default='')
    avatar = models.ImageField('Profile avatar',
                               upload_to=image_upload,
                               null=True,
                               blank=True)
    has_setup = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @classmethod
    def create_profile(cls, user=None):
        if user is not None:
            try:
                cls.objects.create(user=user)
            except ValueError:
                print('Could not create profile.')

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def get_avatar_url(self):
        print('hapennnn')
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        else:
            return alt_avatar_url(self.email.lower())
