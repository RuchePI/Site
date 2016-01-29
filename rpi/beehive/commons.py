from datetime import date, datetime, time, timedelta

from django.db.models import Q

from rpi.beehive.models import Beehive, Readering


def get_personnal_and_public_beehives(user):
    """Find the personnal and the public beehives."""

    beehives = Beehive.objects.all()

    if user and user.is_authenticated():
        personnal_beehives = beehives.filter(owner=user)
        if user.is_superuser:
            public_beehives = beehives.filter(~Q(owner=user))
        else:
            public_beehives = beehives.filter(~Q(owner=user),
                                              Q(public=True))
    else:
        personnal_beehives = None
        public_beehives = beehives.filter(public=True)

    return {
        'personnal_beehives': personnal_beehives,
        'public_beehives': public_beehives
    }


def get_last_readering(beehives):
    """Finds the last readering for each beehives."""

    if beehives is None:
        return beehives

    for b in beehives:
        b.last_readering = Readering.objects.filter(beehive=b) \
                                            .order_by('date').last()
        if b.last_readering is not None:
            b.last_readering.outdoor_humidity *= 100
            b.last_readering.indoor_humidity *= 100


def get_readerings_interval(pk, request):
    """Gets the readering of a beehive between two date."""

    errors = []

    # Tests if the input dates are good.
    from_date = date.today() - timedelta(1)
    to_date = date.today()
    if ('from' in request.GET.keys()) and not (request.GET['from'] == ''):
        try:
            from_date = datetime.strptime(request.GET['from'], '%d-%m-%y') \
                                .date()
        except:
            errors.append("La date du début n'est pas correcte.")
    if ('to' in request.GET.keys()) and not (request.GET['to'] == ''):
        try:
            to_date = datetime.strptime(request.GET['to'], '%d-%m-%y') \
                              .date()
        except:
            errors.append("La date de fin n'est pas correcte.")

    return (
        Readering.objects.filter(
            beehive__id=pk,
            date__range=(
                datetime.combine(from_date, time.min),
                datetime.combine(to_date, time.max)
            )
        ).order_by('date'),
        errors,
        from_date,
        to_date
    )
