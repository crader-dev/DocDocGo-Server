from rest_framework import serializers
from .models import EmergencyRequest


class EmergencyRequestSerializer(serializers.ModelSerializer):
    """
    Maps Emergency Request model to JSON
    """

    class Meta:
        model = EmergencyRequest
        fields = ('id', 'creation_time', 'last_updated', 'status', 'description', 'responding_doctor')
