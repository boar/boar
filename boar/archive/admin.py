from boar.archive.models import Volume, Issue, Part, Page
from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

class VolumeAdmin(OrderedModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('slug', 'title', 'move_up_down_links')

admin.site.register(Volume, VolumeAdmin)

class PartInline(admin.TabularInline):
    model = Part
    prepopulated_fields = {'slug': ('name',)}

class IssueAdmin(admin.ModelAdmin):
    inlines = [PartInline]
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'volume', 'is_published')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'volume', )
    date_hierarchy = 'date'

admin.site.register(Issue, IssueAdmin)

class PageInline(admin.TabularInline):
    model = Page
    extra = 60

class PartAdmin(admin.ModelAdmin):
    inlines = [PageInline]
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Part, PartAdmin)

class PageAdmin(admin.ModelAdmin):
    list_display = ('number', 'part')

admin.site.register(Page, PageAdmin)
