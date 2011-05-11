import datetime
from django.contrib.auth.models import User
from django.db import models

class Cartoon(models.Model):
    date = models.DateField(default=datetime.date.today, unique=True)
    cartoon = models.ImageField(upload_to='cartoons/')
    description = models.TextField(blank=True, null=True)
    author = models.ForeignKey(User, blank=True, null=True)
    
    class Meta:
        get_latest_by = 'date'
        ordering = ('-date',)
    
    def __unicode__(self):
        return unicode(self.date)
    
    def get_absolute_url(self):
        return '/comment/cartoon/%s/%s/%s/' % (self.date.year, self.date.strftime("%b").lower(), self.date.day)

