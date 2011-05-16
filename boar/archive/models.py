from boar.archive.managers import IssueManager
import datetime
from django.core.urlresolvers import reverse
from django.db import models
from ordered_model.models import OrderedModel
import re
import subprocess

class Volume(OrderedModel):
    title = models.CharField(max_length=100, help_text='For example: "Volume 32" or "1973-1974"')
    slug = models.SlugField()
    
    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return self.title


class Issue(models.Model):
    volume = models.ForeignKey(Volume, related_name='issues')
    title = models.CharField(max_length=100, help_text='For example: "Issue 3"')
    slug = models.SlugField()
    date = models.DateField(default=datetime.date.today)
    is_published = models.BooleanField(default=False)
    
    objects = IssueManager()
    
    class Meta:
        ordering = ['-date']
    
    def get_front_page(self):
        try:
            return Page.objects.filter(part__issue=self)[0]
        except IndexError:
            return None
    
    def get_absolute_url(self):
        return reverse('archive_issue', kwargs={
            'volume_slug': self.volume.slug,
            'issue_slug': self.slug,
        })
    
    def __unicode__(self):
        return '%s, %s' % (self.volume, self.title)
        

class Part(models.Model):
    issue = models.ForeignKey(Issue, related_name='parts')
    name = models.CharField(max_length=100, null=True, blank=True, help_text='For example: "Newspaper", "Core" or "One World Week pullout".')
    slug = models.SlugField()
    order = models.IntegerField(default=0)
    
    def get_upload_path(self):
        return 'archive/%s/%s/%s/' % (self.issue.volume.slug, self.issue.slug, self.slug)
    
    def __unicode__(self):
        return '%s in %s' % (self.name, self.issue)
    
    class Meta:
        ordering = ('issue', 'order')


class Page(models.Model):
    part = models.ForeignKey(Part, related_name='pages')
    number = models.IntegerField()
    pdf = models.FileField(upload_to=lambda obj, _: '%s%s.pdf' % (
        obj.part.get_upload_path(),
        obj.number
    ))
    image = models.ImageField(upload_to=lambda obj, _: '%s%s.jpg' % (
        obj.part.get_upload_path(),
        obj.number
    ), editable=False)
    
    class Meta:
        ordering = (
            'part__issue__volume', 
            'part__issue__date', 
            'part__order', 
            'number'
        )
    
    def __unicode__(self):
        return 'Page %s of the %s' % (self.number, self.part)
    
    def get_absolute_url(self):
        return '%s#archive-page-%s-%s' % (
            self.part.issue.get_absolute_url(),
            self.part.pk,
            self.pk,
        )
    
    def save(self, *args, **kwargs):
        # Ensure the PDF is on disk
        super(Page, self).save(*args, **kwargs)
        
        if not subprocess.call(['convert', '-density', '300', unicode(self.pdf.path), '-colorspace', 'RGB', unicode(re.sub(r'\.pdf$', '.jpg', self.pdf.path))]):
            self.image = re.sub(r'\.pdf$', '.jpg', unicode(self.pdf))
            super(Page, self).save(*args, **kwargs)
        
    

