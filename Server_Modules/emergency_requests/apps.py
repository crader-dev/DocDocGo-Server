from django.apps import AppConfig


class EmergencyRequestsConfig(AppConfig):
    name = 'emergency_requests'

    def ready(self):
        # Do not remove. Necessary for registering signals.
        from . import signals
        super(EmergencyRequestsConfig, self).ready()
