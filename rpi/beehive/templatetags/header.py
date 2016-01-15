# coding: utf-8

from django import template
from django.db.models import Q

from rpi.beehive.models import Beehive


register = template.Library()


@register.filter('beehives')
def beehives(user):
    """Gets the beehives accord to user."""

    if user and user.is_authenticated():
        personnal_beehives = Beehive.objects.filter(owner=user)
        if user.is_superuser:
            public_beehives = Beehive.objects.filter(~Q(owner=user))
        else:
            public_beehives = Beehive.objects.filter(~Q(owner=user),
                                                     Q(public=True))
    else:
        personnal_beehives = None
        public_beehives = Beehive.objects.filter(public=True)

    return {'personnal': personnal_beehives, 'public': public_beehives}
