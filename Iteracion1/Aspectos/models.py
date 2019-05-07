from django.db import models

# Create your models here.
class Aspectos(models.Model):
    rubrica_ID  = models.IntegerField(primary_key=True)
    # niv_cumpl   = models.TextField()
    nombre      = models.CharField(max_length=100)