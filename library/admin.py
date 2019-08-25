from django.contrib import admin
from django.utils.html import format_html
from .models import Player, Game


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'created_at' )

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo_tag', 'owners', 'created_at' )

    def logo_tag(self, obj):
        return format_html('<img src="{}" />'.format(obj.get_logo_url()))

    logo_tag.short_description = 'Image'
