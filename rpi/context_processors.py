from django.conf import settings


def app_settings(request):
    """A context processor to access to APP setting."""

    return {'app': settings.RPI_APP}
