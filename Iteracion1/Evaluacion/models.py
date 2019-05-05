import uuid
from django.utils import timezone as tz
from django.db import models

# Create your models here.
class Evaluacion(models.Model):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha_Inicio    = models.DateField(auto_now=False, auto_now_add=False, default=tz.now())
    fecha_Fin       = models.DateField(auto_now=False, auto_now_add=False, default=tz.now())
    is_Open         = models.BooleanField(default=True)