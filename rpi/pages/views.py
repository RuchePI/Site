from django.shortcuts import render

from rpi.beehive.commons import get_personnal_and_public_beehives, \
    get_last_readering


def home(request):
    """Display the home page with the last readering."""

    beehives = get_personnal_and_public_beehives(request.user)
    get_last_readering(beehives['personnal_beehives'])
    get_last_readering(beehives['public_beehives'])

    return render(request, 'home.html', {
        'personnal_beehives': beehives['personnal_beehives'],
        'public_beehives': beehives['public_beehives']
    })


def about_view(request):
    return render(request, 'pages/about.html')
