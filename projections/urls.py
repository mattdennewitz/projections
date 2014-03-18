from django.conf.urls import include, patterns, url


urlpatterns = patterns(
    'projections',

    url(r'^$', 'views.list_players', name='list-players'),
    url(r'^values/$', 'views.player_values', name='player-values'),
)
