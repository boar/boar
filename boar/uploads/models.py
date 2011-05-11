from boar.archive.models import Page
from boar.uploads.manager import UploadManager
import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models, transaction
import os

class Upload(models.Model):
    title = models.CharField(
        help_text="A <strong>thorough</strong> description of what the image is. Include useful keywords so images can be found again in the future.",
        max_length=100)
    upload_date = models.DateTimeField()
    author = models.ForeignKey(User, blank=True, null=True)
    
    objects = UploadManager()
    
    class Meta:
        abstract = True
        ordering = ['-upload_date']
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.upload_date = datetime.datetime.now()
        super(Upload, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title
    
    def get_next_for_author(self):
        qs = self._default_manager.published().filter(
            author=self.author,
            upload_date__gt=self.upload_date,
        ).order_by('upload_date')
        try:
            return qs[0]
        except IndexError:
            return None
    
    def get_previous_for_author(self):
        qs = self._default_manager.published().filter(
            author=self.author,
            upload_date__lt=self.upload_date,
        ).order_by('-upload_date')
        try:
            return qs[0]
        except IndexError:
            return None
    

class ThumbnailSize(models.Model):
    name = models.CharField(max_length=100)
    width = models.IntegerField()
    height = models.IntegerField()
    
    def save(self, *args, **kwargs):
        new = not self.id
        super(ThumbnailSize, self).save(*args, **kwargs) # for size=self
        # Create new thumbnails for all images if this is a new size
        if new:
            for i in Image.objects.all():
                Thumbnail.objects.create(image=i, size=self)
        # Regenerate all the existing thumbnails of this size
        else:
            for t in self.thumbnail_set.all():
                t.save()
                
    def __unicode__(self):
        return "%s (%sx%s)" % (self.name, self.width, self.height)

class Image(Upload):
    upload = models.ImageField(upload_to=settings.UPLOAD_DIRECTORY, help_text='JPEG only.')
    thumbnails = models.ManyToManyField(ThumbnailSize, through='Thumbnail')
    caption = models.CharField(help_text='Caption displayed under the image on the page.', max_length=255, blank=True, null=True)
    page = models.ForeignKey(Page, null=True, blank=True, related_name="images")
    
    def save(self, *args, **kwargs):
        new = not self.id
        update = False
        if self.id:
            update = self.upload != Image.objects.get(id=self.id).upload
        super(Image, self).save(*args, **kwargs)
        # Create thumbnails for new image
        if new:
            for s in ThumbnailSize.objects.all():
                Thumbnail.objects.create(image=self, size=s)
        # Regenerate all existing thumbnails for this image    
        elif update:
            for t in Thumbnail.objects.filter(image=self):
                t.save()
    
    def get_absolute_url(self):
        if not self.author:
            return ''
        return reverse('user_image_detail', kwargs={
            'username': self.author.username,
            'image_id': self.pk,
        })
    
    
class Thumbnail(models.Model):
    image = models.ForeignKey(Image)
    size = models.ForeignKey(ThumbnailSize)
    left = models.IntegerField()
    right = models.IntegerField()
    top = models.IntegerField()
    bottom = models.IntegerField()
    
    @transaction.commit_on_success
    def save(self, *args, **kwargs):
        # Defaults
        if not self.left:
            self.left = 0
        if not self.top:
            self.top = 0
        # We are fixing images which are too large here, because they might be
        # too large but the correct aspect ratio
        if not self.right or self.right > self.image.upload.width:
            self.right = self.image.upload.width
        self.right = self.image.upload.width
        if not self.bottom or self.bottom > self.image.upload.height:
            self.bottom = self.image.upload.height
        # Fix the aspect ratio if it's wrong
        if (float(self.bottom - self.top) / (self.right - self.left)
                > float(self.size.height) / self.size.width):
            self.bottom = int(float(self.size.height) / self.size.width
                            * (self.right - self.left)) + self.top
            # We have run off the bottom, shift the whole thing up
            shift = self.bottom - self.image.upload.height
            if shift > 0:
                self.top -= shift
                self.bottom -= shift
        elif (float(self.bottom - self.top) / (self.right - self.left)
                < float(self.size.height) / self.size.width):
            self.right = int(float(self.size.width) / self.size.height 
                            * (self.bottom - self.top)) + self.left
            # We have run off the right, shift the whole thing left
            shift = self.right - self.image.upload.width
            if shift > 0:
                self.left -= shift
                self.right -= shift
        super(Thumbnail, self).save(*args, **kwargs)
        # Todo: use django.core.files.storage?
        from PIL import Image as PILImage
        im = PILImage.open(self.image.upload.path)
        im = im.crop([self.left, self.top, self.right, self.bottom])
        im = im.resize((self.size.width, self.size.height), PILImage.ANTIALIAS)
        full_path = os.path.join(settings.MEDIA_ROOT, self.get_path())
        directory = os.path.dirname(full_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        im.save(full_path, quality=80)
    
    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.get_path()))
        super(Thumbnail, self).delete(*args, **kwargs)
    
    def get_path(self):
        return os.path.join(
            self.image.upload_date.strftime(self.image.upload.field.upload_to),
            "thumb-%s%s" 
                % (self.id, os.path.splitext(self.image.upload.path)[1]))
    
    def __unicode__(self):
        return unicode(self.size)

