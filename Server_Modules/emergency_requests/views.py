"""Emergency Request Views

Contains the views that relate to emergency requests in the DocDocGo system.

TODO: user auth & permissions -- beyond the scope of this project
"""

from rest_framework import views, generics, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import EmergencyRequest
from .serializers import EmergencyRequestSerializer


class EmergencyRequestViewSet(viewsets.ModelViewSet):
    queryset = EmergencyRequest.objects.all()
    serializer_class = EmergencyRequestSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('status', 'responding_doctor',)
