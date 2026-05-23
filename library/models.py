from django.db import models
from djmoney.models.fields import MoneyField


class Brand(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True)
    founded_year = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class GuitarType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Guitar type'
        verbose_name_plural = 'Guitar types'
        ordering = ['name']

    def __str__(self):
        return self.name


class Guitar(models.Model):
    name = models.CharField(max_length=150)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True)
    guitar_type = models.ForeignKey(GuitarType, on_delete=models.CASCADE, blank=True, null=True)
    price = MoneyField(max_digits=8, decimal_places=2, default=None, default_currency='CZK', null=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='guitars/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
