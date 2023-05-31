import uuid
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings

class BaseAppModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
        
        
image_storage = FileSystemStorage(
    # Physical file location ROOT
    location=settings.MEDIA_PHYSICAL_IMAGES_LOCATION,
    # Url for file
    base_url=settings.MEDIA_URL_IMAGES,
)