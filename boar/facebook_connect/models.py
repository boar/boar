from django.contrib.auth.models import User
from django.db import models

class FacebookProfile(models.Model):
    user = models.OneToOneField(User)
    uid = models.CharField(max_length=255, unique=True)
    
    def __unicode__(self):
            return '%s: %s' % (self.user, self.uid)
