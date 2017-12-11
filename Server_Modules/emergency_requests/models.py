from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class EmergencyRequest(models.Model):
    """
    Stores all related information for an emergency request.
    """
    WAITING = 'WAIT'    # Awaiting approval
    DENIED = 'DENY'     # Denied from DDG system, too severe
    ACCEPTED = 'ACPT'   # Accepted into DDG system, pending doctor response
    REQUESTED = 'RQST'  # Requested doctor's help
    REFUSED = 'RFUS'    # Doctor refused the request
    TIMEDOUT = 'TOUT'   # Doctor response window timed out, stop using DDG
    CONFIRM = 'CNFM'    # Doctor confirmed the request and will be on their way shortly
    ENROUTE = 'ENRT'    # Doctor is on their way to patient
    TREATING = 'TRTG'   # Doctor is treating patient
    COMPLETE = 'COMP'   # Treatment is complete
    STATUS_CODE_CHOICES = (
        (WAITING,   'Waiting'),
        (DENIED,    'Denied'),
        (ACCEPTED,  'Accepted'),
        (REQUESTED, 'Requested'),
        (REFUSED,   'Refused'),
        (TIMEDOUT,  'Timed Out'),
        (CONFIRM,   'Confirmed'),
        (ENROUTE,   'Enroute'),
        (TREATING,  'Treating'),
        (COMPLETE,  'Complete'),
    )
    creation_time = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=4, choices=STATUS_CODE_CHOICES, default=WAITING)
    pain_severity = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1),
                                                                            MaxValueValidator(10)])
    description = models.TextField(max_length=5000)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    # Use unique ForeignKey since OneToOneField requires related field to not be null
    # This will be set to None once the request is complete
    responding_doctor = models.ForeignKey(unique=True, to='doctors.Doctor', blank=True,
                                          null=True, related_name='current_request',
                                          on_delete=models.SET_NULL)
    # This is populated once the request has been completed
    completed_by = models.ForeignKey(to='doctors.Doctor', blank=True, null=True,
                                     related_name='completed_requests', on_delete=models.SET_NULL)
    refusing_doctors = models.ManyToManyField(to='doctors.Doctor', blank=True, related_name='+')

    def set_status(self, status):
        if status in [EmergencyRequest.WAITING, EmergencyRequest.DENIED, EmergencyRequest.ACCEPTED,
                      EmergencyRequest.REFUSED, EmergencyRequest.ENROUTE, EmergencyRequest.CONFIRM,
                      EmergencyRequest.REQUESTED, EmergencyRequest.TIMEDOUT,
                      EmergencyRequest.TREATING, EmergencyRequest.COMPLETE]:
            self.status = status
            self.save()
        else:
            raise AttributeError('Tried to set invalid status on EmergencyRequest: ' + status)

    def set_doctor(self, doctor):
        self.responding_doctor = doctor
        self.save()

    def refuse_responding_doctor(self):
        self.refusing_doctors.add(self.responding_doctor)
        self.responding_doctor = None
        self.status = EmergencyRequest.ACCEPTED
        self.save()

    def complete(self):
        self.completed_by = self.responding_doctor
        self.responding_doctor = None
        self.status = EmergencyRequest.COMPLETE
        self.save()

    def __str__(self):
        return str(self.pk) + ': ' + str(self.description)
