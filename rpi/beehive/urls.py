from django.conf.urls import url

from rpi.beehive.views import AddBeehiveView, DeleteBeehiveView, \
    ModifyBeehiveView


urlpatterns = [
    url(r'^ajouter/$', AddBeehiveView.as_view(), name='add-beehive'),
    url(r'^(?P<pk>\d+)/modifier$', ModifyBeehiveView.as_view(),
        name='modify-beehive'),
    url(r'^(?P<pk>\d+)/supprimer$', DeleteBeehiveView.as_view(),
        name='delete-beehive'),
]
