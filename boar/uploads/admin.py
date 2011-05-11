from django.contrib import admin
from boar.uploads.forms import ThumbInlineForm
from boar.uploads.models import Image, Thumbnail, ThumbnailSize

class UploadAdmin(admin.ModelAdmin):
    exclude = ('upload_date',)
    list_display = ('title', 'upload_date', 'author')
    date_hierarchy = 'upload_date'
    search_fields = ('title',)
    raw_id_fields = ('author', 'page')


class ThumbnailInline(admin.StackedInline):
    model = Thumbnail
    extra = 0
    template = 'uploads/inline.html'
    form = ThumbInlineForm


class ImageAdmin(UploadAdmin):
    inlines = [ThumbnailInline,]
    list_display = ('title', 'caption', 'upload_date', 'author')
    
    def queryset(self, request):
        qs = super(UploadAdmin, self).queryset(request)
        if super(ImageAdmin, self).has_change_permission(request):
            return qs
        else:
            return qs.filter(author=request.user)
    
    def has_change_permission(self, request, obj=None):
        if not obj:
            return True # So they can see the change list page
        if obj.author == request.user or super(ImageAdmin, self).has_change_permission(request, obj):
            return True
        else:
            return False

admin.site.register(Image, ImageAdmin)


class ThumbnailSizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'width', 'height')

admin.site.register(ThumbnailSize, ThumbnailSizeAdmin)


