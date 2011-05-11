from django.contrib.auth.models import User
from django.db import models
from boar.utils.unique_slugify import unique_slugify
import re

class UserProfileManager(models.Manager):
    def create_from_name(self, name):
        u = User()
        try:
            u.first_name, u.last_name = name.split(None, 1)
        except ValueError:
            u.first_name, u.last_name = name, ''
        unique_slugify(u,
            re.sub(r'[^a-z0-9\.]', '', '.'.join(name.lower().split())),
            slug_field_name='username',
            slug_separator='.',
            slugify=False)
        u.set_unusable_password()
        u.save()
        return self.create(user=u)
    
