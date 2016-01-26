# coding: utf-8

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from rpi.beehive.models import Beehive, Readering
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


def summary_view(request, pk):
    current = get_object_or_404(Beehive, pk=pk)

    if current.owner != request.user and not request.user.is_superuser \
            and not current.public:
        raise PermissionDenied

    try:
        last_readering = Readering.objects.filter(beehive=current) \
                                          .latest('date')
        last_readering.outdoor_humidity *= 100
        last_readering.indoor_humidity *= 100
    except Readering.DoesNotExist:
        last_readering = None

    return render(request, 'beehive/summary.html', {
        'current': current,
        'last_readering': last_readering
    })


class ListReaderingView(ListView):
    """Makes the table with the beehive's readering and paginates it."""

    model = Readering
    context_object_name = 'readerings'
    template_name = 'beehive/table.html'
    paginate_by = 30

    def dispatch(self, request, *args, **kwargs):
        current = get_object_or_404(Beehive, pk=self.kwargs['pk'])
        if current.owner != request.user and not request.user.is_superuser \
                and not current.public:
            raise PermissionDenied

        return super(ListReaderingView, self).dispatch(request, *args,
                                                       **kwargs)

    def get_queryset(self):
        readerings = Readering.objects.filter(beehive__id=self.kwargs['pk'])
        for r in readerings:
            r.outdoor_humidity *= 100
            r.indoor_humidity *= 100
        return readerings

    def get_context_data(self, *args, **kwargs):
        context = super(ListReaderingView, self).get_context_data(*args,
                                                                  **kwargs)
        context['current'] = Beehive.objects.get(pk=self.kwargs['pk'])
        return context


def delete_readering_view(request, pk):
    """Deletes a readering passing in id arguments."""

    current = get_object_or_404(Readering, pk=pk)

    if current.beehive.owner != request.user and not request.user.is_superuser:
        raise PermissionDenied

    current.delete()

    return redirect(reverse('table', kwargs={'pk': current.beehive.pk}))
