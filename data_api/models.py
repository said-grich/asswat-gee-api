from django.db import models

# Create your models here.


class NdviModel(models.Model):
    geojson_polygon = models.CharField(max_length=255)
    date = models.DateField()
