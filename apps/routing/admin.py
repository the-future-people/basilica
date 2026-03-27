from django.contrib import admin
from .models import Routeplan, RoutePlanStop


class RoutePlanStopInline(admin.TabularInline):
    model = RoutePlanStop
    extra = 0
    readonly_fields = ['id', 'distance_from_previous_km', 'estimated_arrival']
    fields = ['order', 'bin', 'fill_level_at_generation', 'battery_level_at_generation', 'distance_from_previous_km', 'estimated_arrival']


@admin.register(Routeplan)
class RoutePlanAdmin(admin.ModelAdmin):
    list_display = ['circuit', 'scheduled_for', 'trigger_type', 'status', 'total_bins_selected', 'total_bins_in_circuit', 'selection_rate', 'fill_threshold_used', 'estimated_duration_minutes']
    list_filter = ['status', 'trigger_type', 'circuit']
    search_fields = ['circuit__name', 'circuit__code']
    readonly_fields = ['id', 'created_at', 'updated_at', 'generated_at', 'dispatched_at']
    inlines = [RoutePlanStopInline]

    fieldsets = (
        ('Route Info', {
            'fields': ('id', 'circuit', 'trip', 'trigger_type', 'triggered_by')
        }),
        ('Status', {
            'fields': ('status', 'failure_reason')
        }),
        ('Metrics', {
            'fields': ('total_bins_in_circuit', 'total_bins_selected', 'fill_threshold_used', 'estimated_duration_minutes', 'estimated_distance_km')
        }),
        ('Timing', {
            'fields': ('scheduled_for', 'generated_at', 'dispatched_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(RoutePlanStop)
class RoutePlanStopAdmin(admin.ModelAdmin):
    list_display = ['route_plan', 'bin', 'order', 'fill_level_at_generation', 'distance_from_previous_km', 'estimated_arrival']
    list_filter = ['route_plan__circuit']
    search_fields = ['bin__serial_number']
    readonly_fields = ['id']