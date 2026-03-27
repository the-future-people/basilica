from django.contrib import admin
from .models import Bin, BinTelemetry


@admin.register(Bin)
class BinAdmin(admin.ModelAdmin):
    list_display = ['serial_number', 'device_eui', 'bin_type', 'status', 'is_online', 'fill_level', 'circuit', 'last_seen']
    list_filter = ['status', 'bin_type', 'is_online', 'circuit']
    search_fields = ['serial_number', 'device_eui', 'location_description']
    readonly_fields = ['id', 'created_at', 'updated_at', 'last_seen', 'is_online']
    ordering = ['-created_at']

    fieldsets = (
        ('Identity', {
            'fields': ('id', 'serial_number', 'device_eui', 'bin_type')
        }),
        ('Location', {
            'fields': ('circuit', 'latitude', 'longitude', 'location_description')
        }),
        ('Specs & Status', {
            'fields': ('capacity_litres', 'status', 'is_online', 'last_seen')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(BinTelemetry)
class BinTelemetryAdmin(admin.ModelAdmin):
    list_display = ['bin', 'fill_level', 'battery_level', 'is_tampered', 'signal_strength', 'recorded_at']
    list_filter = ['is_tampered', 'bin__circuit']
    search_fields = ['bin__serial_number']
    readonly_fields = ['id', 'received_at']
    ordering = ['-recorded_at']