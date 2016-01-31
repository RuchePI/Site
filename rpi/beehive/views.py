# coding: utf-8

import csv

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from rpi.beehive.commons import get_readerings_interval
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

        return redirect(reverse('summary', args=[current.pk]))


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
        readerings = Readering.objects.filter(beehive__id=self.kwargs['pk']) \
                                      .order_by('-date')
        for r in readerings:
            r.outdoor_humidity *= 100
            r.indoor_humidity *= 100
        return readerings

    def get_context_data(self, *args, **kwargs):
        context = super(ListReaderingView, self).get_context_data(*args,
                                                                  **kwargs)
        context['current'] = Beehive.objects.get(pk=self.kwargs['pk'])
        return context


class ChartReaderingView(ListReaderingView):
    """Makes the charts."""

    template_name = 'beehive/charts.html'
    paginate_by = None

    def get_queryset(self):
        """Gets the readerings of a period."""

        readerings, _, _, _ = get_readerings_interval(self.kwargs['pk'],
                                                      self.request)
        for r in readerings:
            r.outdoor_humidity *= 100
            r.indoor_humidity *= 100

        return readerings

    def get_context_data(self, *args, **kwargs):
        context = super(ChartReaderingView, self).get_context_data(*args,
                                                                   **kwargs)

        _, errors, from_date, to_date = get_readerings_interval(
            self.kwargs['pk'], self.request
        )
        context['errors'] = errors
        context['from_date'] = from_date
        context['to_date'] = to_date

        if 'from' in self.request.GET.keys():
            context['arg_from'] = self.request.GET['from']
        if 'to' in self.request.GET.keys():
            context['arg_to'] = self.request.GET['to']

        return context


def export_view(request, pk):
    """Exports the readerings of a beehive."""

    current = get_object_or_404(Beehive, pk=pk)

    if current.owner != request.user and not request.user.is_superuser:
        raise PermissionDenied

    readerings, errors, _, _ = get_readerings_interval(pk, request)

    if 'from' in request.GET.keys():
        from_date = request.GET['from']
    else:
        from_date = ''
    if 'to' in request.GET.keys():
        to_date = request.GET['to']
    else:
        to_date = ''

    if ('format' in request.GET.keys()):
        # CSV export.
        if request.GET['format'] == 'csv':
            if ('delimiter' in request.GET.keys()):
                if request.GET['delimiter'] != '':
                    if len(request.GET['delimiter']) == 1:
                        delimiter = request.GET['delimiter']
                    else:
                        errors.append("Le délimiteur doit faire un seul "
                                      "caractère.")
                else:
                    errors.append("Un délimiteur doit être renseigné.")
                delimiter = request.GET['delimiter']
            else:
                delimiter = ''

            if 'decimal_separator' in request.GET.keys():
                if request.GET['decimal_separator'] != '':
                    decimal_separator = request.GET['decimal_separator']
                else:
                    errors.append("Un séparateur décimal doit être renseigné.")
                decimal_separator = request.GET['decimal_separator']
            else:
                decimal_separator = ''

            def format_float(number):
                return str(number).replace('.', decimal_separator)

            if errors:
                return render(request, 'beehive/export.html', {
                    'current': current,
                    'errors': errors,
                    'from': from_date,
                    'to': to_date,
                    'delimiter': delimiter,
                    'decimal_separator': decimal_separator
                })

            # Make the file.
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; ' \
                'filename="beehive_{}.csv'.format(pk)

            writer = csv.writer(response, delimiter=delimiter)
            writer.writerow([
                "Date",
                "Température extérieure (°C)",
                "Température intérieure (°C)",
                "Température dans l'essaim (°C)",
                "Humidité intérieure (%)",
                "Humidité extérieure (%)",
                "Masse (kg)"
            ])

            for r in readerings:
                writer.writerow([
                    '{}/{}/{} {}:{}:{}'.format(r.date.day, r.date.month,
                                               r.date.year, r.date.hour,
                                               r.date.minute, r.date.second),
                    format_float(r.outdoor_temperature),
                    format_float(r.indoor_temperature),
                    format_float(r.swarm_temperature),
                    format_float(r.outdoor_humidity),
                    format_float(r.indoor_humidity),
                    format_float(r.weight)
                ])

            return response

    return render(request, 'beehive/export.html', {'current': current})


def delete_readering_view(request, pk):
    """Deletes a readering passing in id arguments."""

    current = get_object_or_404(Readering, pk=pk)

    if current.beehive.owner != request.user and not request.user.is_superuser:
        raise PermissionDenied

    current.delete()

    return redirect(reverse('table', kwargs={'pk': current.beehive.pk}))
