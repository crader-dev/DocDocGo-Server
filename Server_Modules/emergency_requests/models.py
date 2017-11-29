from django.db import models


class EmergencyRequest(models.Model):
    """
    Stores all related information for an emergency request.
    """
    WAITING = 'WAIT'
    ACCEPTED = 'ACPT'
    TREATING = 'TRTG'
    COMPLETE = 'COMP'
    STATUS_CODE_CHOICES = (
        (WAITING, 'Waiting'),
        (ACCEPTED, 'Accepted'),
        (TREATING, 'Treating'),
        (COMPLETE, 'Complete'),
    )

    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=4, choices=STATUS_CODE_CHOICES, default=WAITING)
    description = models.TextField(max_length=5000)
    # TODO: voice recording (optional)
    responding_doctor = models.OneToOneField(to='Doctor', related_name='serviced_by',
                                             blank=True)
