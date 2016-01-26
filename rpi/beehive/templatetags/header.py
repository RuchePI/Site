from django import template

from rpi.beehive.commons import get_personnal_and_public_beehives, \
    get_last_readering


register = template.Library()


@register.filter('beehives')
def beehives(user):
    """Gets the beehives accord to user."""

    beehives = get_personnal_and_public_beehives(user)

    return {
        'personnal': beehives['personnal_beehives'],
        'public': beehives['public_beehives']
    }
