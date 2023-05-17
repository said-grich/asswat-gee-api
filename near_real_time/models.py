from django.db import models


class NDVI(models.Model):
    ndvi = models.TextField()  # NDVI values as a serialized string
    date = models.DateField()  # Date of the NDVI data
    product = models.CharField(max_length=10)  # Product name
    # Geometry field representing the location (point, polygon, etc.)
    geometry = models.TextField()
    def __str__(self):
        return f"NDVI object ({self.date})"

    class Meta:
        verbose_name = "NDVI"
        verbose_name_plural = "NDVI Data"
