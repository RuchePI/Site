from rest_framework import serializers

from rpi.beehive.models import Readering


class ReaderingSerializer(serializers.ModelSerializer):
    """The serializer of Readering's model."""

    class Meta:
        model = Readering
        fields = ('outdoor_temperature', 'indoor_temperature',
                  'swarm_temperature', 'outdoor_humidity', 'indoor_humidity',
                  'weigth')
