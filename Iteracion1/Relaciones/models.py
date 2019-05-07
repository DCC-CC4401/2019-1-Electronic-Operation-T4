from django.db import models

# Create your models here.
class Usuario_Evaluacion(models.Model):
    id_Usuario      = models.ForeignKey('Usuario.Usuario', on_delete=models.CASCADE, blank=False, null=False)
    id_Evaluación   = models.ForeignKey('Evaluacion.Evaluacion', on_delete=models.CASCADE, blank=False, null=False)

class Evaluacion_Equipo(models.Model):
    id_Evaluación   = models.ForeignKey('Evaluacion.Evaluacion', on_delete=models.CASCADE, blank=False, null=False)
    id_Equipo       = models.ForeignKey('Equipo.Equipo', on_delete=models.CASCADE, blank=False, null=False)

class Rubrica_Resumen(models.Model):
    id_Rúbrica = models.ForeignKey('Rubrica.Rubrica', on_delete=models.CASCADE, blank=False, null=False)
    id_Resumen = models.ForeignKey('Resumen.Resumen', on_delete=models.CASCADE, blank=False, null=False)