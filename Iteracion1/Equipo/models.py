import uuid
from django.db import models

#from ..Curso.models import Curso

# Create your models here.
class Equipo(models.Model):
    id       = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    #id_curso = models.ForeignKey('Curso', on_delete=models.CASCADE, blank=False, null=False)
    número   = models.PositiveSmallIntegerField(blank=False, null=False, default=1)
    nombre   = models.CharField(blank=False, null=False, default='Grupo 1', max_length=100)
    #class Meta:
    #    unique_together = [['id_curso', 'número']]