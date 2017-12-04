"""DocDocGo API Endpoints

Contains all root level endpoints for the DocDocGo versioned API.
"""

from django.conf.urls import url, include

urlpatterns = [
    # Endpoints for DocDocGo API Version 0
    url(r'v0/', include([
        url(r'doctors/',  include('doctors.urls')),
        url(r'requests/', include('emergency_requests.urls')),
    ], namespace='v0')),
]
