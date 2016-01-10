from django.conf.urls import url

from rpi.user.views import login_view, logout_view, RegisterView, \
                           new_password_view, warning_unregister_view, \
                           unregister_view


urlpatterns = [
    url(r'^connexion/$', login_view),
    url(r'^deconnexion/$', logout_view),
    url(r'^nouveau/$', RegisterView.as_view(), name='register-user'),
    url(r'^mot-de-passe/$', new_password_view),
    url(r'^suppresion/confirmation/$', warning_unregister_view),
    url(r'^suppresion/validation/$', unregister_view),
]
