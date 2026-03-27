from rest_framework import serializers
from django.contrib.auth.models import User
from apps.drivers.models import Driver, Trip, TripStop


class DriverUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class DriverSerializer(serializers.ModelSerializer):
    user = DriverUserSerializer(read_only=True)
    circuit_name = serializers.CharField(source='circuit.name', read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Driver
        fields = [
            'id', 'user', 'full_name', 'circuit', 'circuit_name',
            'phone_number', 'ghana_card_number',
            'status', 'is_on_trip',
            'last_active_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'is_on_trip', 'last_active_at', 'created_at', 'updated_at']

    def get_full_name(self, obj):
        return obj.user.get_full_name()


class TripStopSerializer(serializers.ModelSerializer):
    bin_serial = serializers.CharField(source='bin.serial_number', read_only=True)
    bin_location = serializers.CharField(source='bin.location_description', read_only=True)
    bin_latitude = serializers.DecimalField(source='bin.latitude', max_digits=9, decimal_places=6, read_only=True)
    bin_longitude = serializers.DecimalField(source='bin.longitude', max_digits=9, decimal_places=6, read_only=True)

    class Meta:
        model = TripStop
        fields = [
            'id', 'order', 'bin', 'bin_serial', 'bin_location',
            'bin_latitude', 'bin_longitude',
            'fill_level_at_dispatch', 'status',
            'collected_at', 'notes'
        ]
        read_only_fields = ['id', 'order', 'fill_level_at_dispatch', 'collected_at']


class TripSerializer(serializers.ModelSerializer):
    stops = TripStopSerializer(many=True, read_only=True)
    driver_name = serializers.SerializerMethodField()
    circuit_name = serializers.CharField(source='circuit.name', read_only=True)
    completion_rate = serializers.ReadOnlyField()

    class Meta:
        model = Trip
        fields = [
            'id', 'driver', 'driver_name', 'circuit', 'circuit_name',
            'status', 'scheduled_date', 'started_at', 'completed_at',
            'total_bins_planned', 'total_bins_collected', 'completion_rate',
            'stops', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'started_at', 'completed_at',
            'total_bins_planned', 'total_bins_collected',
            'created_at', 'updated_at'
        ]

    def get_driver_name(self, obj):
        return obj.driver.user.get_full_name()


class TripListSerializer(serializers.ModelSerializer):
    driver_name = serializers.SerializerMethodField()
    circuit_name = serializers.CharField(source='circuit.name', read_only=True)
    completion_rate = serializers.ReadOnlyField()

    class Meta:
        model = Trip
        fields = [
            'id', 'driver_name', 'circuit_name', 'status',
            'scheduled_date', 'total_bins_planned',
            'total_bins_collected', 'completion_rate'
        ]

    def get_driver_name(self, obj):
        return obj.driver.user.get_full_name()