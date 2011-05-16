from boar.editorial_board.models import Position, PositionName, PositionMember
from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

class PositionNameInline(admin.TabularInline):
    model = PositionName
    prepopulated_fields = {'slug': ('name',)}

class PositionMemberInline(admin.TabularInline):
    model = PositionMember
    raw_id_fields = ('user',)

class PositionAdmin(OrderedModelAdmin):
    inlines = [PositionNameInline, PositionMemberInline]
    list_display = ('__unicode__', 'move_up_down_links')

#admin.site.register(Position, PositionAdmin)

