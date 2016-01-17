# coding: utf-8

import uuid

from django.contrib.auth.models import User
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
