from boar.mailing_lists.models import MailingList, Mailing
from django.contrib import admin
from django.db import models
from ordered_model.admin import OrderedModelAdmin

class MailingListAdmin(OrderedModelAdmin):
    list_display = ('name', 'from_email', 'description', 'default_for_new_users', 'is_visible', 'subscriber_count',  'move_up_down_links')
    list_editable = ['is_visible']
    filter_horizontal = ('subscribers',)
    
    def subscriber_count(self, obj):
        return obj.subscribers__count
    
    def queryset(self, request):
        return super(MailingListAdmin, self).queryset(request).annotate(models.Count('subscribers'))

admin.site.register(MailingList, MailingListAdmin)

class MailingAdmin(admin.ModelAdmin):
    list_display = ('subject', 'mailing_list', 'date_sent')
    fields = ('mailing_list', 'subject', 'message')
    list_filter = ('mailing_list',)
    date_hierarchy = 'date_sent'
    search_fields = ('subject',)

admin.site.register(Mailing, MailingAdmin)
