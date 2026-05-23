from django.contrib import admin
from .models import Guitar


@admin.register(Guitar)

class GuitarAdmin(admin.ModelAdmin):
    list_display = ('name', 'guitar_type', 'price', 'updated_at')
    search_fields = ('name', 'guitar_type', 'price', 'description')
    list_filter = ('guitar_type', 'price')
    ordering = ('name',)
    readonly_fields = ('updated_at',)
