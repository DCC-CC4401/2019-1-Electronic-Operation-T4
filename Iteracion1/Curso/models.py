import uuid
from django.db import models

# Create your models here.
class Curso(models.Model):
    SEMESTRE_CHOICES = (
        (1, 'Otoño'),
        (2, 'Primavera'),
        (3, 'Verano')
    )
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    código          = models.CharField(max_length=20)
    número_seccion  = models.PositiveSmallIntegerField(default=1)
    año             = models.IntegerField()
    semestre        = models.SmallIntegerField(choices=SEMESTRE_CHOICES, default=1)
    class Meta:
        unique_together = [['código', 'número_seccion', 'año', 'semestre']]