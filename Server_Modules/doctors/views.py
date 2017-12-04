"""Doctor Views

Contains the views that relate to doctors in the DocDocGo system.

TODO: user auth & permissions -- beyond the scope of this project
"""

from rest_framework import views, generics, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import Doctor
from .serializers import DoctorSerializer


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('status', 'first_name', 'last_name')
