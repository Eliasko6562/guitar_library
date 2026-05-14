from django.db import models


class Guitar(models.Model):
    class GuitarType(models.TextChoices):
        CLASSICAL = 'Classical'
        ELECTRIC = 'Electric'
        ACOUSTIC = 'Acoustic'
        ELECTROACOUSTIC = 'Electroacoustic'
        BASS = 'Bass'

    name = models.CharField(max_length=150)
    guitar_type = models.CharField(max_length=20, choices=GuitarType.choices, default=GuitarType.CLASSICAL)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='guitars/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
