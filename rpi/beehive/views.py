# coding: utf-8

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, UpdateView

from rpi.beehive.models import Beehive
from rpi.beehive.forms import BeehiveForm


class AddBeehiveView(CreateView):
    """Adds a beehive."""

    form_class = BeehiveForm
    template_name = 'beehive/add.html'

    # Makes this view only reachable by login user.
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AddBeehiveView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        current = Beehive(
            name=form.data.get('name'),
            owner=self.request.user,
            public=False,
        )
        if form.data.get('public'):
            current.public = True
        current.save()

        return redirect(reverse('home'))


class ModifyBeehiveView(UpdateView):
    """Modifies a beehives."""

    form_class = BeehiveForm
    template_name = 'beehive/modify.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """Makes this view only reachable by the beehive's owner and the super
        user."""

        self.object = self.get_object()
        if self.object.owner != request.user and not request.user.is_superuser:
            raise PermissionDenied

        return super(ModifyBeehiveView, self).dispatch(request, *args,
                                                       **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(Beehive, pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse('modify-beehive', kwargs={'pk': self.object.pk})


class DeleteBeehiveView(DeleteView):
    """Deletes a beehives."""

    template_name = 'beehive/delete.html'
    success_url = reverse_lazy('home')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """Does the same as above."""

        self.object = self.get_object()
        if self.object.owner != request.user and not request.user.is_superuser:
            raise PermissionDenied

        return super(DeleteBeehiveView, self).dispatch(request, *args,
                                                       **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(Beehive, pk=self.kwargs['pk'])
