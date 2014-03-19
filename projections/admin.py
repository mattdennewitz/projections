from __future__ import unicode_literals

from django.contrib import admin

from projections.models import Batting, Pitching


def fg_link(obj):
    return (
        '<a href="http://www.fangraphs.com/statss.aspx?playerid=' + obj.playerid + '"'
        + 'target="_blank">View on FG</a>'
    )
fg_link.allow_tags = True


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'playerid', fg_link, 'pos', 'is_kept', )
    list_editable = ('is_kept', )
    list_filter=('pos', )
    search_fields=('name', )


admin.site.register(Batting, PlayerAdmin)
admin.site.register(Pitching, PlayerAdmin)
