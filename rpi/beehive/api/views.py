from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rpi.beehive.models import Beehive
from rpi.beehive.api.serializers import ReaderingSerializer


@api_view(['POST', ])  # Authorizes only POST requests.
def readering_detail(request, pk):
    """Creates a readering."""

    try:
        beehive = Beehive.objects.get(pk=pk)
    except Beehive.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Test if it is the good token.
    if not request.POST['token']:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    elif str(beehive.token) == request.POST['token']:
        serializer = ReaderingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(beehive=beehive)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)
