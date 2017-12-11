from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import EmergencyRequest
from . import request_handling


@receiver(post_save, sender=EmergencyRequest)
def handle_request_change(instance, **kwargs):
    status = instance.status
    if status == EmergencyRequest.ACCEPTED and instance.responding_doctor is None:
        # Select & Notify doctors
        request_handling.assign_doctor(instance)
        if instance.responding_doctor is None:
            request_handling.requeue_request(instance)
    # elif status == EmergencyRequest.REQUESTED:
    #     pass
    elif status == EmergencyRequest.REFUSED:
        instance.refuse_responding_doctor()
    # elif status == EmergencyRequest.DENIED:
    #     pass
    # elif status == EmergencyRequest.TIMEDOUT:
    #     pass
    # elif status == EmergencyRequest.CONFIRM:  # TODO: Or should we use ENROUTE?
    #     pass
    elif status == EmergencyRequest.COMPLETE and instance.responding_doctor is not None:
        instance.complete()
