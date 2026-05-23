from unfold.admin import ModelAdmin
from django.contrib import admin
from .models import Brand, Guitar, GuitarType

admin.site.site_url = '/'


@admin.register(Brand)
class BrandAdmin(ModelAdmin):
    list_display = ('name', 'country', 'founded_year')
    search_fields = ('name', 'country')
    ordering = ('name',)


@admin.register(GuitarType)
class GuitarTypeAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Guitar)
class GuitarAdmin(ModelAdmin):
    list_display = ('name', 'brand', 'guitar_type', 'price', 'updated_at')
    search_fields = ('name', 'brand__name', 'guitar_type__name', 'price', 'description')
    list_filter = ('brand', 'guitar_type', 'price')
    ordering = ('name',)
    readonly_fields = ('updated_at',)
