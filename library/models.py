from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MinLengthValidator
from django.utils import timezone
from decimal import Decimal
import re
from djmoney.models.fields import MoneyField


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True, validators=[MinLengthValidator(2)])
    country = models.CharField(max_length=100, blank=True)
    founded_year = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def clean(self):
        errors = {}
        # Validate founded_year is realistic
        if self.founded_year:
            current_year = timezone.now().year
            if self.founded_year < 1700 or self.founded_year > current_year:
                errors['founded_year'] = f'Founded year must be between 1700 and {current_year}.'

        # Validate country if provided: prefer pycountry lookup, fallback to regex/length
        if self.country:
            country_val = self.country.strip()
            # try pycountry for authoritative validation
            try:
                import pycountry
                try:
                    pycountry.countries.lookup(country_val)
                except (LookupError, KeyError):
                    errors['country'] = 'Country not recognized. Use official country name or ISO code (e.g., "CZ" or "Czech Republic").'
            except Exception:
                # fallback: require ISO country code (alpha-2 or alpha-3) when pycountry unavailable
                if not re.match(r'^[A-Za-z]{2,3}$', country_val):
                    errors['country'] = 'Country not recognized and pycountry not installed; provide ISO alpha-2 or alpha-3 code (e.g., "CZ").'

        if errors:
            raise ValidationError(errors)


class GuitarType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Guitar type'
        verbose_name_plural = 'Guitar types'
        ordering = ['name']

    def __str__(self):
        return self.name

    def clean(self):
        # Ensure name has some minimal length
        if not self.name or len(self.name.strip()) < 3:
            raise ValidationError({'name': 'Guitar type name must be at least 3 characters long.'})


class Guitar(models.Model): 
    name = models.CharField(max_length=150)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True)
    guitar_type = models.ForeignKey(GuitarType, on_delete=models.CASCADE, blank=True, null=True)
    price = MoneyField(
        max_digits=8,
        decimal_places=2,
        default=None,
        default_currency='CZK',
        null=True,
        validators=[MinValueValidator(Decimal('0.00'))],
    )
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='guitars/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def clean(self):
        errors = {}
        # name
        if not self.name or not self.name.strip():
            errors['name'] = 'Name cannot be blank.'

        # price: MoneyField validator should handle negative values but double-check
        if self.price is not None:
            try:
                amount = self.price.amount if hasattr(self.price, 'amount') else Decimal(self.price)
            except Exception:
                amount = None
            if amount is None:
                errors['price'] = 'Invalid price.'
            elif amount < Decimal('0.00'):
                errors['price'] = 'Price cannot be negative.'

        # image: check size and basic format if available
        if self.image:
            try:
                # file size check (5 MB limit)
                max_size = 5 * 1024 * 1024
                file_size = getattr(self.image, 'size', None)
                if file_size is None and hasattr(self.image, 'file'):
                    file_size = getattr(self.image.file, 'size', None)
                if file_size and file_size > max_size:
                    errors['image'] = 'Image file too large (max 5MB).'
                # optional: try to detect image format via Pillow if installed
                try:
                    from PIL import Image
                    self.image.file.seek(0)
                    img = Image.open(self.image.file)
                    if img.format not in ('JPEG', 'PNG', 'GIF'):
                        errors.setdefault('image', 'Unsupported image format (allowed: JPEG, PNG, GIF).')
                    img.close()
                    self.image.file.seek(0)
                except Exception:
                    # if Pillow isn't available or image can't be opened, skip strict format check
                    pass
            except Exception:
                errors.setdefault('image', 'Invalid image.')

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        # Ensure model validation runs on save
        self.full_clean()
        super().save(*args, **kwargs)
