from django.dispatch import receiver
from django.db.models.signals import post_delete

from videofiles.models import VideoFile

@receiver(post_delete, sender=VideoFile)
def post_delete_video_file_on_cdn(sender, instance, *args, **kwargs):
    if not isinstance(sender, VideoFile):
        return
    if not instance.file:
        return
    try:
        instance.file.delete(save=False)
    except:
        pass
    
