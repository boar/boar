from boar.accounts.manager import UserProfileManager
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    about = models.TextField(blank=True, null=True)
    phone_number = models.CharField(blank=True, null=True, max_length=255)
    photo = models.ImageField(upload_to='profile-pictures/', blank=True, null=True)
    articles_graph = models.ImageField(upload_to='graphs/user_articles/', blank=True, null=True, editable=False)
    
    objects = UserProfileManager()
    
    def __unicode__(self):
        return unicode(self.user)
    
    def get_position_description(self):
        positions = [p.name for p in self.user.position_set.all()]
        sections = ['%s Editor' % s.title for s in self.user.section_set.all()]
        return ', '.join(positions + sections)

    def set_name(self, name):
        try:
            self.user.first_name, self.user.last_name = name.split(None, 1)
        except ValueError:
            self.user.first_name, self.user.last_name = name, ''
        self.user.save()

