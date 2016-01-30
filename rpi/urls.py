from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

import rpi.pages.views
import rpi.user.urls
import rpi.beehive.urls
import rpi.pages.urls


urlpatterns = [
    url(r'^$', rpi.pages.views.home, name='home'),
    url(r'^utilisateurs/', include('rpi.user.urls')),
    url(r'^ruches/', include('rpi.beehive.urls')),
    url(r'^pages/', include('rpi.pages.urls')),
    url(r'^admin/', admin.site.urls),

    # API
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^api/', include('rpi.beehive.api.urls')),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
