from django.conf import settings


def app_settings(request):
    """
    A context processor to have access to APP setting.
    """
    return {'app': settings.RPI_APP}
