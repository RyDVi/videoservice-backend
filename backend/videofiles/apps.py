from django.apps import AppConfig
from django.db.models.signals import post_delete

class VideofilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'videofiles'
    
    def ready(self):
        # Implicitly connect signal handlers decorated with @receiver.
        from . import signals
        # Explicitly connect a signal handler.
        post_delete.connect(signals.post_delete_video_file_on_cdn)
