from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

import rpi.pages.views
import rpi.user.urls


urlpatterns = [
    url(r'^$', rpi.pages.views.home, name='home'),
    url(r'utilisateurs/', include('rpi.user.urls')),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
