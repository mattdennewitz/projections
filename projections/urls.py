from django.conf.urls import include, patterns, url


urlpatterns = patterns(
    'projections',

    url(r'^$', 'views.list_players', name='list-players'),

    # api
    url(r'^api/players/$', 'api_v1.list_players', name='api-list-players'),
)
