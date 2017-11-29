from django.conf.urls import url, include

urlpatterns = [
    # Endpoints for DocDocGo API Version 0
    url(r'^v0/', include([
        url(r'^doctors/(?P<id>[0-9]+)', ),
        url(r'^requests/(?P<id>[0-9]+)', ),
    ], namespace='v0')),
]
