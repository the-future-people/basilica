from rest_framework import serializers
from apps.circuits.models import Circuit


class CircuitSerializer(serializers.ModelSerializer):
    total_bins = serializers.ReadOnlyField()
    active_bins = serializers.ReadOnlyField()

    class Meta:
        model = Circuit
        fields = [
            'id', 'name', 'code', 'description', 'status',
            'center_latitude', 'center_longitude',
            'total_bins', 'active_bins',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CircuitListSerializer(serializers.ModelSerializer):
    total_bins = serializers.ReadOnlyField()
    active_bins = serializers.ReadOnlyField()

    class Meta:
        model = Circuit
        fields = ['id', 'name', 'code', 'status', 'total_bins', 'active_bins']