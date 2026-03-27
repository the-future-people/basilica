from django.contrib import admin
from .models import Circuit


@admin.register(Circuit)
class CircuitAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'status', 'total_bins', 'active_bins', 'created_at']
    list_filter = ['status']
    search_fields = ['name', 'code']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['name']

    fieldsets = (
        ('Identity', {
            'fields': ('id', 'code', 'name', 'description')
        }),
        ('Location', {
            'fields': ('center_latitude', 'center_longitude')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )