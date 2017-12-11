from rest_framework import serializers
from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    """
    Maps Doctor model to JSON
    """

    class Meta:
        model = Doctor
        fields = ('id', 'status', 'first_name', 'last_name', 'phone_number', 'latitude',
                  'longitude', 'house_call_radius', 'current_request', 'completed_requests')
