from boar.archive.models import Volume, Issue, Part, Page
from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

class VolumeAdmin(OrderedModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('slug', 'title', 'move_up_down_links')
    fieldsets = (
        (None, {
            'fields': ('title',)
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('slug',)
        }),
    )

admin.site.register(Volume, VolumeAdmin)

class PartInline(admin.TabularInline):
    model = Part
    prepopulated_fields = {'slug': ('name',)}

class IssueAdmin(admin.ModelAdmin):
    inlines = [PartInline]
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'volume', 'date', 'is_published')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'volume', )
    date_hierarchy = 'date'
    fieldsets = (
        (None, {
            'fields': ('volume', 'title', 'date', 'is_published')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('slug',)
        }),
    )
    

admin.site.register(Issue, IssueAdmin)

class PageInline(admin.TabularInline):
    model = Page
    extra = 60

class PartAdmin(admin.ModelAdmin):
    inlines = [PageInline]
    list_display = ('name', 'issue')
    list_filter = ('issue__title', 'issue__volume__title')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Part, PartAdmin)

class PageAdmin(admin.ModelAdmin):
    list_display = ('number', 'get_part', 'get_issue')
    list_filter = ('part__name', 'part__issue__title', 'part__issue__volume__title')
    ordering = ('-part__issue__date',)
    raw_id_fields = ('part',)

    def get_part(self, obj):
        return obj.part.name
    get_part.short_description = 'Part'

    def get_issue(self, obj):
        return obj.part.issue
    get_issue.short_description = 'Issue'

admin.site.register(Page, PageAdmin)

