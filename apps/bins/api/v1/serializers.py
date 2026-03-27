from rest_framework import serializers
from apps.bins.models import Bin, BinTelemetry


class BinTelemetrySerializer(serializers.ModelSerializer):
    class Meta:
        model = BinTelemetry
        fields = [
            'id', 'bin', 'fill_level', 'battery_level',
            'temperature', 'is_tampered', 'signal_strength',
            'recorded_at', 'received_at'
        ]
        read_only_fields = ['id', 'received_at']


class BinSerializer(serializers.ModelSerializer):
    fill_level = serializers.ReadOnlyField()
    latest_telemetry = BinTelemetrySerializer(read_only=True)
    circuit_name = serializers.CharField(source='circuit.name', read_only=True)

    class Meta:
        model = Bin
        fields = [
            'id', 'device_eui', 'serial_number', 'bin_type',
            'latitude', 'longitude', 'location_description',
            'circuit', 'circuit_name', 'capacity_litres',
            'status', 'is_online', 'last_seen',
            'fill_level', 'latest_telemetry',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'is_online', 'last_seen', 'created_at', 'updated_at']


class BinListSerializer(serializers.ModelSerializer):
    fill_level = serializers.ReadOnlyField()
    circuit_name = serializers.CharField(source='circuit.name', read_only=True)

    class Meta:
        model = Bin
        fields = [
            'id', 'serial_number', 'bin_type', 'status',
            'is_online', 'fill_level', 'circuit', 'circuit_name',
            'location_description', 'latitude', 'longitude'
        ]