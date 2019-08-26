from django.contrib import admin
from admin_auto_filters.filters import AutocompleteFilter
from django.utils.html import format_html
from .models import Player, Game, GameStat


class GameFilter(AutocompleteFilter):
    title = 'Game'
    field_name = 'game'


class PlayerFilter(AutocompleteFilter):
    title = 'Player'
    field_name = 'player'


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'avatar_tag', 'games_count', 'playing_count', 'finished_count', 'created_at')

    search_field = 'nickname'

    def avatar_tag(self, obj):
        return format_html('<img src="{}" />'.format(obj.avatar_url))

    avatar_tag.short_description = 'Avatar'

    def games_count(self, obj):
        return obj.games.count()

    def playing_count(self, obj):
        return 'TBD'

    def finished_count(self, obj):
        return 'TBD'


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo_tag', 'owners', 'created_at')

    search_fields = ['name']

    def logo_tag(self, obj):
        return format_html('<img src="{}" />'.format(obj.get_logo_url()))

    logo_tag.short_description = 'Logo'


@admin.register(GameStat)
class GameStatAdmin(admin.ModelAdmin):
    list_display = ('player', 'game', 'playtime')
    list_filter = ['player', GameFilter]

    class Media:
        pass
