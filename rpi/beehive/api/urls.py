from django.conf.urls import url

from rpi.beehive.api.views import readering_detail


urlpatterns = [
    url(r'^ruches/(?P<pk>\d+)$', readering_detail),
]
