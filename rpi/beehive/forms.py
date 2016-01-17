from django import forms

from rpi.beehive.models import Beehive


class BeehiveForm(forms.ModelForm):
    """Form to add and modify a beehive."""

    class Meta:
        model = Beehive
        fields = ['name', 'public']

    name = forms.CharField(
        label=u"Nom de la ruche",
        required=True,
        max_length=100,
    )

    public = forms.BooleanField(
        label=u"Publique ?",
        required=False,
    )
