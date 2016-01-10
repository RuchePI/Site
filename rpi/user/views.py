# coding: utf-8

from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import CreateView

from rpi.user.forms import LoginForm, RegisterForm, NewPasswordForm


def login_view(request):
    """Logs in user."""

    error = False

    # If the form is not empty.
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)

                # Redirect user to the home.
                return redirect(reverse('rpi.pages.views.home'))
            else:
                error = True
    else:
        form = LoginForm()

    return render(request, 'user/login.html', {'form': form, 'error': error})


def logout_view(request):
    """Logs out user."""

    logout(request)
    request.session.clear()
    return redirect(reverse('rpi.pages.views.home'))


class RegisterView(CreateView):
    """Creates an user."""

    model = User
    form_class = RegisterForm
    template_name = 'user/register.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
        user = User.objects.create_user(
            username=form.data.get('username'),
            password=form.data.get('password'),
        )
        return render(self.request, 'user/register_sucess.html')


@login_required
def new_password_view(request):
    """Creates a new password."""

    if request.method == 'POST':
        form = NewPasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            password = form.cleaned_data['password']

            user.set_password(password)
            user.save()

            return render(request, 'user/new_password_sucess.html')
    else:
        form = NewPasswordForm()

    return render(request, 'user/new_password.html', {'form': form})


@login_required
def warning_unregister_view(request):
    """Displays a warning page before the deletion of the user."""

    return render(request, 'user/unregister.html', {'user': request.user})


@login_required
def unregister_view(request):
    """Deletes the user."""

    current = request.user

    # If the user isn't the last.
    if not User.objects.count() == 1:
        User.objects.filter(pk=current.pk).delete()
    else:
        return render(request, 'user/unregister_fail.html')

    return redirect(reverse('rpi.pages.views.home'))
