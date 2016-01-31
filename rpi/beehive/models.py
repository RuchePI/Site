# coding: utf-8

import uuid

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Beehive(models.Model):
    """A beehive."""

    class Meta:
        verbose_name = "Ruche"
        verbose_name_plural = "Ruches"

    name = models.CharField(
        "Nom de la ruche",
        max_length=100,
    )

    owner = models.ForeignKey(User)

    public = models.BooleanField(
        "La ruche est-elle publique ?",
        default=True,
    )

    token = models.UUIDField(
        "Jeton",
        default=uuid.uuid4,
        editable=False,
    )

    def __str__(self):
        return '{} ({})'.format(self.name, self.owner)


class Readering(models.Model):
    """Readerings from the beehives."""

    class Meta:
        verbose_name = "Relevé"
        verbose_name_plural = "Relevés"

    date = models.DateTimeField(
        "Date",
        auto_now_add=True,
    )

    beehive = models.ForeignKey(Beehive)

    outdoor_temperature = models.FloatField("Température extérieure")

    indoor_temperature = models.FloatField("Température intérieure")

    swarm_temperature = models.FloatField("Température dans l'essaim")

    outdoor_humidity = models.FloatField(
        "Humidité extérieure",
        validators=[MinValueValidator(0), MaxValueValidator(1)],
    )

    indoor_humidity = models.FloatField(
        "Humidité intérieure",
        validators=[MinValueValidator(0), MaxValueValidator(1)],
    )

    weight = models.FloatField(
        "Masse",
        validators=[MinValueValidator(0)],
    )

    def __str__(self):
        return '{} - {}'.format(self.date, self.beehive)
