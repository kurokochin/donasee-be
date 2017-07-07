import collections

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse


def PUBLIC_APIS(r, f):
    return [
        # user
        ('register', reverse('register', request=r, format=f)),
        ('login', reverse('login', request=r, format=f)),
    ]

@api_view(('GET',))
@permission_classes((AllowAny,))
def api_root(request, format=None):
    """
    GET:
    Display all available urls.

    Since some urls have specific permissions, you might not be able to access
    them all.
    """
    apis = PUBLIC_APIS(request, format)
    return Response(collections.OrderedDict(apis))