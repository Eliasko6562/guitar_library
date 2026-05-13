from django.contrib import admin
from .models import Guitar


@admin.register(Guitar)
class GuitarAdmin(admin.ModelAdmin):
    list_display = ('name', 'guitar_type', 'created_at')
    search_fields = ('name', 'guitar_type', 'description')
    list_filter = ('guitar_type',)
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')
