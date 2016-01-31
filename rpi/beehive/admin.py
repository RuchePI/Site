from django.contrib import admin

from rpi.beehive.models import Beehive, Readering


class BeehiveAdmin(admin.ModelAdmin):
    """Represention of Beehive model in the admin interface."""

    list_display = ('pk', 'name', 'owner', 'public', 'token')


class ReaderingAdmin(admin.ModelAdmin):
    """Represention of Readering model in the admin interface."""

    list_display = ('pk', 'date', 'beehive', 'outdoor_temperature',
                    'indoor_temperature', 'swarm_temperature',
                    'outdoor_humidity', 'indoor_humidity', 'weight')


admin.site.register(Beehive, BeehiveAdmin)
admin.site.register(Readering, ReaderingAdmin)
