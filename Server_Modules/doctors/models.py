from django.db import models
from django.core.validators import RegexValidator

PHONE_NUMBER_REGEX = RegexValidator(regex='^\+?[0-9]{8,15}', message='Phone number must contain '
                                                                     'only digits (0-9) and can '
                                                                     'optionally begin with +.')


class Doctor(models.Model):
    """
    Collection of information about a particular active DocDocGo doctor.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(validators=PHONE_NUMBER_REGEX, max_length=16)
    # In miles, 0 = unlimited
    house_call_radius = models.PositiveSmallIntegerField()
    # TODO: location (use django-location-field package?)
    current_request = models.OneToOneField(to='EmergencyRequest', related_name='responding_to',
                                           blank=True)

    def __str__(self):
        return self.first_name + self.last_name