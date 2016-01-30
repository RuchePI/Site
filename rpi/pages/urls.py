from django.conf.urls import url

from rpi.pages.views import about_view

urlpatterns = [
    url(r'^a-propos$', about_view, name='about'),
]
