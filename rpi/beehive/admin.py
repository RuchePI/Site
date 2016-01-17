from django.contrib import admin

from rpi.beehive.models import Beehive


class BeehiveAdmin(admin.ModelAdmin):
    """Represention of Beehive model in the admin interface."""

    list_display = ('pk', 'name', 'owner', 'public', 'token')


admin.site.register(Beehive, BeehiveAdmin)
