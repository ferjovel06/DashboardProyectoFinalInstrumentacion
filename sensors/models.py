from django.db import models

class Measure(models.Model):
    """
    Model to store sensors data.
    """
    timestamp = models.DateTimeField(auto_now_add=True)
    velocidad_motor = models.IntegerField()
    caudal = models.FloatField(null=True, blank=True)
    cant_botellas = models.IntegerField(default=0)

    def __str__(self):
        return f"Measures at {self.timestamp}: Velocidad Motor = {self.velocidad_motor}"

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
