import datetime
from django import forms
from django.contrib.auth.models import User
from django.db import models

class Ceremony(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    thanks_message = models.TextField(default="You're awesome. Thanks for voting. Be sure to join us at the awards ceremony!", help_text="Message displayed after a vote has been cast.")
    start_date = models.DateTimeField(default=datetime.datetime.now)
    end_date = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'ceremonies'


class Award(models.Model):
    ceremony = models.ForeignKey(Ceremony, related_name="awards")
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name
    

class Nominee(models.Model):
    award = models.ForeignKey(Award, related_name="nominees")
    name = models.CharField(max_length=255)
    order = models.CharField(max_length=255, help_text="Ordering field")
    link = models.URLField(blank=True, null=True)
    
    class Meta:
        ordering = ['order']
    
    def __unicode__(self):
        return self.name


class Vote(models.Model):
    user = models.ForeignKey(User)
    nominee = models.ForeignKey(Nominee)
    date = models.DateTimeField(default=datetime.datetime.now)

