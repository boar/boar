from django import forms
from django.conf import settings
from django.contrib.gis import admin
from django.db import models
from django.utils.http import urlquote_plus
from ordered_model.admin import OrderedModelAdmin
from reversion.admin import VersionAdmin
from taggit.models import Tag as TaggitTag

from boar.articles.forms import ArticleAdminModelForm
from boar.articles.models import *
from boar.articles.widgets import MarkItUpWidget
from boar.common.admin import OSMGeoStackedInline

class SectionAdmin(OrderedModelAdmin):
    list_display = ('title', 'menu_item', 'email', 'move_up_down_links')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('editors',)

admin.site.register(Section, SectionAdmin)


class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('members',)

admin.site.register(Position, PositionAdmin)

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug', 'created')
    search_fields = ('name',)
    formfield_overrides = {
        models.TextField: {'widget': MarkItUpWidget},
    }

admin.site.unregister(TaggitTag)
admin.site.register(Tag, TagAdmin)

######################################
# Metadata inlines
######################################

class MetadataInline(admin.StackedInline):
    extra = 1
    max_num = 1

class BookMetadataInline(MetadataInline):
    model = BookMetadata

class GameMetadataInline(MetadataInline):
    model = GameMetadata

class LiveBlogMetadataInline(MetadataInline):
    model = LiveBlogMetadata

class MusicAlbumMetadataInline(MetadataInline):
    model = MusicAlbumMetadata

class MusicLiveMetadataInline(MetadataInline):
    model = MusicLiveMetadata

class PodcastMetadataInline(MetadataInline):
    model = PodcastMetadata

class TravelMetadataInline(OSMGeoStackedInline):
    model = TravelMetadata
    extra = 1
    max_num = 1

class ArticleAdmin(VersionAdmin):
    date_hierarchy = 'pub_date'
    # tags field is also filter_horizontal - forced in forms.py
    filter_horizontal = ('authors',)
    form = ArticleAdminModelForm
    inlines = [
        BookMetadataInline,
        GameMetadataInline,
        LiveBlogMetadataInline,
        MusicAlbumMetadataInline,
        MusicLiveMetadataInline,
        PodcastMetadataInline,
        TravelMetadataInline,
    ]
    list_display = ('title', 'section', 'tone', 'get_tags', 'pub_date', 'published', 'featured')
    list_filter = ('published', 'featured', 'section', 'tone')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('image', 'page')
    search_fields = ('title',)
    fieldsets = (
        (None, {
            'fields': ('title', 'summary', 'body', 'image', 'tags', 'section', 'published', 'featured', 'authors', 'score', 'notes')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('slug', 'pub_date', 'page')
        }),
        ('Tone', {
            'fields': ('tone',)
        }),
    )
    
    def get_tags(self, obj):
        return ', '.join(t.name for t in obj.tags.all())
    
    class Media:
        js = (
            'static/js/src/jquery-1.3.2.min.js',
            'static/js/article-admin.js',
        )
    
    # Fill in bits of information when using "save and add another"
    # def _alter_response(self, request, obj, response):
    #     if request.POST.has_key('_addanother'):
    #         response['Location'] = '%s?published=1&section=%s&pub_date=%s' % (
    #             response['Location'],
    #             urlquote_plus(obj.section.pk),
    #             urlquote_plus(obj.pub_date),
    #         )
    #     
    # def response_add(self, request, obj, *args, **kwargs):
    #     response = super(ArticleAdmin, self).response_add(request, obj, *args, **kwargs)
    #     self._alter_response(request, obj, response)
    #     return response
    # 
    # def response_change(self, request, obj, *args, **kwargs):
    #     response = super(ArticleAdmin, self).response_change(request, obj, *args, **kwargs)
    #     self._alter_response(request, obj, response)
    #     return response

admin.site.register(Article, ArticleAdmin)


