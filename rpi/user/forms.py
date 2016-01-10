# coding: utf-8

from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    """Form to connect an user."""

    username = forms.CharField(
        label=u"Nom d'utilisateur",
        max_length=30,
        required=True,
    )

    password = forms.CharField(
        label=u"Mot de passe",
        widget=forms.PasswordInput,
        required=True,
    )


class RegisterForm(forms.ModelForm):
    """Form to register a new user."""

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm']

    username = forms.CharField(
        label=u"Nom d'utilisateur",
        max_length=30,
        required=True,
    )

    password = forms.CharField(
        label=u"Mot de passe",
        min_length=8,
        widget=forms.PasswordInput,
        required=True,
    )

    password_confirm = forms.CharField(
        label=u"Confirmation du mot de passe",
        min_length=8,
        widget=forms.PasswordInput,
        required=True,
    )

    def clean(self):
        """Tests if both passwords are the same."""

        cleaned_data = super(RegisterForm, self).clean()

        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if not password == password_confirm:
            msg = u"Les mots de passe sont différents."
            self._errors['password_confirm'] = self.error_class([msg])

        return cleaned_data


class NewPasswordForm(forms.Form):
    """Defines a new password."""

    password = forms.CharField(
        label=u"Mot de passe",
        min_length=8,
        widget=forms.PasswordInput,
        required=True,
    )

    password_confirm = forms.CharField(
        label=u"Confirmation du mot de passe",
        min_length=8,
        widget=forms.PasswordInput,
        required=True,
    )

    def clean(self):
        """Tests if both passwords are the same."""

        cleaned_data = super(NewPasswordForm, self).clean()

        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if not password == password_confirm:
            msg = u"Les mots de passe sont différents."
            self._errors['password_confirm'] = self.error_class([msg])

        return cleaned_data
