from boar.awards.models import Ceremony, Award, Nominee
from django.contrib import admin

admin.site.register(Ceremony)

class NomineeInline(admin.TabularInline):
    model = Nominee

class AwardAdmin(admin.ModelAdmin):
    inlines = [NomineeInline]

admin.site.register(Award, AwardAdmin)

