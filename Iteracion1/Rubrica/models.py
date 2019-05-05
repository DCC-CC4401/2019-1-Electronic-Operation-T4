import uuid
from django.utils import timezone as tz
from django.db import models

# Create your models here.
class Rubrica(models.Model):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rúbrica         = models.FileField(upload_to=None, max_length=100)
    duración_Mínima = models.TimeField(blank=False, null=False, default=tz.now())
    duración_Máxima = models.TimeField(blank=False, null=False, default=tz.now())