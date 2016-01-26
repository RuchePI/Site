from django.conf.urls import url

from rpi.beehive.views import AddBeehiveView, delete_readering_view, \
    ListReaderingView, DeleteBeehiveView, ModifyBeehiveView, summary_view


urlpatterns = [
    url(r'^ajouter/$', AddBeehiveView.as_view(), name='add-beehive'),
    url(r'^(?P<pk>\d+)/voir/$', summary_view, name='summary'),
    url(r'^(?P<pk>\d+)/voir/tableau/$', ListReaderingView.as_view(),
        name='table'),
    url(r'^(?P<pk>\d+)/modifier$', ModifyBeehiveView.as_view(),
        name='modify-beehive'),
    url(r'^(?P<pk>\d+)/supprimer$', DeleteBeehiveView.as_view(),
        name='delete-beehive'),
    url(r'^supprimer-releve/(?P<pk>\d+)$', delete_readering_view,
        name='delete-readering'),
]
