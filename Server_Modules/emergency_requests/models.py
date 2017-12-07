from django.db import models


class EmergencyRequest(models.Model):
    """
    Stores all related information for an emergency request.
    """
    WAITING = 'WAIT'   # Awaiting approval
    DENIED = 'DENY'    # Denied from DDG system, too severe
    ACCEPTED = 'ACPT'  # Accepted into DDG system, pending doctor response
    TIMEDOUT = 'TOUT'  # Doctor response window timed out, stop using DDG
    ENROUTE = 'ENRT'   # Doctor accepted request and is on their way to patient
    TREATING = 'TRTG'  # Doctor is treating patient
    COMPLETE = 'COMP'  # Treatment is complete
    STATUS_CODE_CHOICES = (
        (WAITING,  'Waiting'),
        (DENIED,   'Denied'),
        (ACCEPTED, 'Accepted'),
        (TIMEDOUT, 'Timed Out'),
        (ENROUTE,  'Enroute'),
        (TREATING, 'Treating'),
        (COMPLETE, 'Complete'),
    )

    creation_time = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=4, choices=STATUS_CODE_CHOICES, default=WAITING)
    description = models.TextField(max_length=5000)
    # TODO: location (use django-location-field package?)
    # TODO: voice recording (optional)
    responding_doctor = models.OneToOneField(to='doctors.Doctor', blank=True, null=True)

    def __str__(self):
        return self.pk + ': ' + self.description
