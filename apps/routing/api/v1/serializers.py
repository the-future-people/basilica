from rest_framework import serializers
from apps.routing.models import Routeplan, RoutePlanStop


class RoutePlanStopSerializer(serializers.ModelSerializer):
    bin_serial = serializers.CharField(source='bin.serial_number', read_only=True)
    bin_location = serializers.CharField(source='bin.location_description', read_only=True)
    bin_latitude = serializers.DecimalField(source='bin.latitude', max_digits=9, decimal_places=6, read_only=True)
    bin_longitude = serializers.DecimalField(source='bin.longitude', max_digits=9, decimal_places=6, read_only=True)

    class Meta:
        model = RoutePlanStop
        fields = [
            'id', 'order', 'bin', 'bin_serial', 'bin_location',
            'bin_latitude', 'bin_longitude',
            'fill_level_at_generation', 'battery_level_at_generation',
            'distance_from_previous_km', 'estimated_arrival'
        ]
        read_only_fields = ['id']


class RoutePlanSerializer(serializers.ModelSerializer):
    stops = RoutePlanStopSerializer(many=True, read_only=True)
    circuit_name = serializers.CharField(source='circuit.name', read_only=True)
    selection_rate = serializers.ReadOnlyField()

    class Meta:
        model = Routeplan
        fields = [
            'id', 'circuit', 'circuit_name', 'trip',
            'trigger_type', 'triggered_by', 'status', 'failure_reason',
            'total_bins_in_circuit', 'total_bins_selected',
            'fill_threshold_used', 'selection_rate',
            'estimated_duration_minutes', 'estimated_distance_km',
            'scheduled_for', 'generated_at', 'dispatched_at',
            'stops', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'generated_at', 'dispatched_at',
            'created_at', 'updated_at'
        ]


class RoutePlanListSerializer(serializers.ModelSerializer):
    circuit_name = serializers.CharField(source='circuit.name', read_only=True)
    selection_rate = serializers.ReadOnlyField()

    class Meta:
        model = Routeplan
        fields = [
            'id', 'circuit_name', 'trigger_type', 'status',
            'total_bins_selected', 'total_bins_in_circuit',
            'selection_rate', 'scheduled_for', 'generated_at'
        ]