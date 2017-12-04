"""Doctors URL Configuration

Contains the URL patterns for endpoints specific to emergency requests. These
patterns should be included by ddg_api.urls.
"""

from rest_framework.routers import SimpleRouter

from . import views

# Use a router instead of explicit routes to take advantage of ViewSets
router = SimpleRouter()
router.register(r'', views.DoctorViewSet)

urlpatterns = router.urls
