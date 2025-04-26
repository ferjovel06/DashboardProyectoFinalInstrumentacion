from django.db import models

class Measures(models.Model):
    """
    Model to store sensors data.
    """
    timestamp = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField()
    ph = models.FloatField()
    tds = models.FloatField()
    ec = models.FloatField(null=True, blank=True)  # Optional field for electrical conductivity

    def __str__(self):
        return f"Measures at {self.timestamp}: Temperature={self.temperature}, pH={self.ph}, TDS={self.tds}"

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Measurement"
        verbose_name_plural = "Measurements"
