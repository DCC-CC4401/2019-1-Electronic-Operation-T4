from django.db import models
import uuid

# Create your models here.
class Estudiante(models.Model):

    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    historial          = models.CharField(max_length=20)
    Presentó        =    models.BooleanField(default=False)
    nombre        = models.CharField(max_length=20)
    Notas        = models.CharField(max_length=20)

