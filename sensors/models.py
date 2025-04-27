from django.db import models

class Measure(models.Model):
    """
    Model to store sensors data.
    """
    timestamp = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField()
    ph = models.FloatField()
    tds = models.FloatField()
    ec = models.FloatField(null=True, blank=True)  # Optional field for electrical conductivity
    motor_ph_alcalino = models.BooleanField(default=False)
    motor_ph_acido = models.BooleanField(default=False)
    motor_tds_altos = models.BooleanField(default=False)

    def __str__(self):
        return f"Measures at {self.timestamp}: Temperature={self.temperature}, pH={self.ph}, TDS={self.tds}"

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Measurement"
        verbose_name_plural = "Measurements"


class Suggestion(models.Model):
    """
    Model to store suggestions about the system.
    """
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='suggestions/', null=True, blank=True)

    def __str__(self):
        return f"Suggestion: {self.title} - {self.subtitle}"

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Suggestion"
        verbose_name_plural = "Suggestions"
