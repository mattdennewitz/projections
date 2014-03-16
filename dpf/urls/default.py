from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin


urlpatterns = patterns(
    '',

    url(r'^', include('projections.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if hasattr(settings, 'SERVE_FILES') and settings.SERVE_FILES:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
