from boar.accounts.models import UserProfile
from boar.articles.models import Article
from boar.cartoons.models import Cartoon
from boar.facebook_connect.models import FacebookProfile
from boar.mailing_lists.models import MailingList
from boar.uploads.models import Image
from django import forms, template
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from django.contrib.comments.models import Comment
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.text import truncate_words
from django.utils.translation import ugettext as _
import re

class RawIdWidget(forms.TextInput):
    """
    A Widget for displaying model selects in the "raw_id" interface rather than
    in a <select> box.
    """
    def __init__(self, model, attrs=None):
        self.model = model
        super(RawIdWidget, self).__init__(attrs)
 
    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        related_url = '../../../%s/%s/' % (self.model._meta.app_label, self.model._meta.object_name.lower())
        if not attrs.has_key('class'):
            attrs['class'] = 'vForeignKeyRawIdAdminField' # The JavaScript looks for this hook.
        output = [super(RawIdWidget, self).render(name, value, attrs)]
        # TODO: "id_" is hard-coded here. This should instead use the correct
        # API to determine the ID dynamically.
        output.append('<a href="%s" class="related-lookup" id="lookup_id_%s" onclick="return showRelatedObjectLookupPopup(this);"> ' % \
            (related_url, name))
        output.append('<img src="%simg/admin/selector-search.gif" width="16" height="16" alt="%s" /></a>' % (settings.ADMIN_MEDIA_PREFIX, _('Lookup')))
        if value:
            output.append(self.label_for_value(value))
        return mark_safe(u''.join(output))
 
    def label_for_value(self, value):
        obj = self.model._default_manager.get(pk=value)
        return '&nbsp;<strong>%s</strong>' % escape(truncate_words(obj, 14))


class MergeUserForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=RawIdWidget(User))
    victims = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.MultipleHiddenInput)


class AddWriterForm(forms.Form):
    full_name = forms.CharField()
        
    def save(self, commit=True):
        return UserProfile.objects.create_from_name(
            self.cleaned_data['full_name']
        ).user


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    extra = 1
    max_num = 1

class FacebookProfileInline(admin.StackedInline):
    model = FacebookProfile
    extra = 1
    max_num = 1

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User

class AccountsUserAdmin(UserAdmin):
    change_list_template = "admin/auth/user_change_list.html"
    inlines = [UserProfileInline, FacebookProfileInline]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_facebook_account')
    actions = ['merge_user_action']
    form = UserChangeForm
    
    def is_facebook_account(self, obj):
        try:
            obj.facebookprofile
        except FacebookProfile.DoesNotExist:
            return False
        else:
            return True
    is_facebook_account.boolean = True
        
    def get_urls(self):
        from django.conf.urls.defaults import patterns
        return patterns('',
            (r'^add-writer/$', self.admin_site.admin_view(self.add_writer_view)),
            (r'^merge-users/$', self.admin_site.admin_view(self.merge_user_view)),
        ) + super(AccountsUserAdmin, self).get_urls()
    
    def add_view(self, request):
        if '_popup' in request.REQUEST:
            return self.add_writer_view(request)
        else:
            return super(AccountsUserAdmin, self).add_view(request)
    
    def has_change_permission(self, request, obj=None):
        if not obj:
            return True # So they can see the change list page
        if obj == request.user or self.has_change_permission(request):
            return True
        else:
            return False
    
    def add_writer_view(self, request):
        # See UserAdmin
        if not self.has_add_permission(request):
            raise PermissionDenied
        if request.method == 'POST':
            form = AddWriterForm(request.POST)
            if form.is_valid():
                new_user = form.save()
                msg = _('The %(name)s "%(obj)s" was added successfully.') % {'name': 'user', 'obj': new_user}
                self.log_addition(request, new_user)
                if "_addanother" in request.POST:
                    request.user.message_set.create(message=msg)
                    return HttpResponseRedirect(request.path)
                elif '_popup' in request.REQUEST:
                    return self.response_add(request, new_user)
                else:
                    request.user.message_set.create(message=msg + ' ' + _("You may edit it again below."))
                    return HttpResponseRedirect('../%s/' % new_user.id)
        else:
            form = AddWriterForm()
        return render_to_response('admin/auth/add_writer_form.html', {
            'title': _('Add writer'),
            'form': form,
            'is_popup': '_popup' in request.REQUEST,
            'add': True,
            'change': False,
            'has_add_permission': True,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_file_field': False,
            'has_absolute_url': False,
            'auto_populated_fields': (),
            'opts': self.model._meta,
            'save_as': False,
            'username_help_text': self.model._meta.get_field('username').help_text,
            'root_path': self.admin_site.root_path,
            'app_label': self.model._meta.app_label,            
        }, context_instance=template.RequestContext(request))
    
    def merge_user_view(self, request):
        if request.method == 'POST':
            form = MergeUserForm(request.POST)
            if form.is_valid():
                user = form.cleaned_data['user']
                for victim in form.cleaned_data['victims']:
                    # Simple stuff
                    for group in victim.groups.all():
                        if group not in user.groups.all():
                            user.groups.add(group)
                    if victim.email and not user.email:
                        user.email = victim.email
                    if victim.is_staff and not user.is_staff:
                        user.is_staff = True
                    if victim.is_superuser and not user.is_superuser:
                        user.is_superuser = True
                    if victim.is_active and not user.is_active:
                        user.is_active = True
                    
                    # Transfer profile if user merging into doesn't have profile
                    # but victim does
                    try:
                        profile = user.get_profile()
                    except UserProfile.DoesNotExist:
                        try:
                            profile = victim.get_profile()
                        except UserProfile.DoesNotExist:
                            pass
                        else:
                            profile.user = user
                            profile.save()
                    try:
                        profile = user.facebookprofile
                    except FacebookProfile.DoesNotExist:
                        try:
                            profile = victim.facebookprofile
                        except FacebookProfile.DoesNotExist:
                            pass
                        else:
                            profile.user = user
                            profile.save()
                    # Articles
                    for a in Article.objects.filter(authors=victim):
                        a.authors.remove(victim)
                        if not a.authors.filter(pk=user.pk):
                            a.authors.add(user)
                        a.save()
                    Image.objects.filter(author=victim).update(author=user)
                    LogEntry.objects.filter(user=victim).update(user=user)
                    Cartoon.objects.filter(author=victim).update(author=user)
                    # Mailing lists
                    for ml in MailingList.objects.filter(subscribers=victim):
                        ml.subscribers.remove(victim)
                        if not ml.subscribers.filter(pk=user.pk):
                            ml.subscribers.add(user)
                        ml.save()
                    Comment.objects.filter(user=victim).update(
                        user=user)
                    
                    User.objects.get(pk=victim.pk).delete()
                user.save()
                self.message_user(request, "Users successfully merged into %s." % form.cleaned_data['user'].username)
                return HttpResponseRedirect('../')
        elif 'victims' in request.GET:
            form = MergeUserForm(initial={'victims': request.GET['victims'].split(',')})
        else:
            return HttpResponseRedirect('../')
        return render_to_response('admin/auth/merge_user_form.html', {
            'title': _('Merge users'),
            'form': form,
            'is_popup': '_popup' in request.REQUEST,
            'add': True,
            'change': False,
            'has_add_permission': True,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_file_field': False,
            'has_absolute_url': False,
            'auto_populated_fields': (),
            'opts': self.model._meta,
            'save_as': False,
            'root_path': self.admin_site.root_path,
            'app_label': self.model._meta.app_label,
        }, context_instance=template.RequestContext(request))
        
    
    def merge_user_action(self, request, queryset):
        return HttpResponseRedirect('merge-users/?victims=%s' % ','.join(unicode(o.id) for o in queryset))
    merge_user_action.short_description = 'Merge selected users into another user'

admin.site.unregister(User)
admin.site.register(User, AccountsUserAdmin)
