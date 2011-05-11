from boar.cartoons.models import Cartoon
from django.contrib import admin

class CartoonAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('date', 'author')
    raw_id_fields = ('author',)
    search_fields = ('description',)

admin.site.register(Cartoon, CartoonAdmin)
