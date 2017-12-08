import threading
import time
from django.utils import timezone

from doctors.models import Doctor
from .models import EmergencyRequest
from .util.geospatial import haversine_distance


REQUEST_TIMEOUT_LIMIT = 60  # Time (in seconds) before request will be timed out
POLLING_FREQUENCY = 20  # Delay (in seconds) between polls for re-queued requests


def assign_doctor(request):
    # Check all available doctors to see if there are any nearby
    nearest_doctor = None
    nearest_dist = 0
    for doc in Doctor.objects.filter(status=Doctor.ONLINE, current_request__isnull=True):
        dist = haversine_distance(doc.latitude, doc.longitude, request.latitude, request.longitude)
        if dist <= doc.house_call_radius and (nearest_doctor is None or dist < nearest_dist):
            nearest_doctor = doc

    # A doctor is found and they are sent the request
    if nearest_doctor is not None:
        # notify doctor
        request.set_doctor(nearest_doctor)
        request.set_status(EmergencyRequest.REQUESTED)


# NOTE: This is not very scalable, but it fits our needs for this project. If this were put this
#       into production, then we would build a more robust request routing system and use something
#       like Celery + RabbitMQ for background tasks, etc.
def requeue_request(request):
    def poll_doctor_assignment(req):
        while req.responding_doctor is None:
            time.sleep(POLLING_FREQUENCY)

            # Make sure the request hasn't timed out
            if (timezone.now() - request.creation_time).total_seconds() >= REQUEST_TIMEOUT_LIMIT:
                request.set_status(EmergencyRequest.TIMEDOUT)
                return

            assign_doctor(request)

    thread = threading.Thread(target=poll_doctor_assignment, args=[request])
    thread.setDaemon(True)
    thread.start()
