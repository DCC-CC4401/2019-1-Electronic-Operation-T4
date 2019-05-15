import uuid
from django.conf import settings
from django.utils import timezone as tz
from django.db import models
# Create your models here.
class Rubrica(models.Model):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre          = models.CharField(blank=False, default='Nombre de rúbrica', max_length=100)
    rúbrica         = models.FileField(upload_to='../media/', max_length=100)
    duración_Mínima = models.TimeField(blank=False, null=False, default=tz.now())
    duración_Máxima = models.TimeField(blank=False, null=False, default=tz.now())
    class Meta:
        unique_together = [['id', 'nombre']]