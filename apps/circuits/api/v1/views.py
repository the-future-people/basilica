from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.circuits.models import Circuit
from apps.core_auth.permissions import IsSystemAdmin, IsDriverOrCircuitAdmin
from .serializers import CircuitSerializer, CircuitListSerializer


class CircuitViewSet(viewsets.ModelViewSet):
    queryset = Circuit.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return CircuitListSerializer
        return CircuitSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsSystemAdmin()]
        return [IsAuthenticated(), IsDriverOrCircuitAdmin()]

    def get_queryset(self):
        user = self.request.user
        queryset = Circuit.objects.all()

        # Drivers only see their own circuit
        if hasattr(user, 'driver_profile') and not user.is_staff:
            queryset = queryset.filter(id=user.driver_profile.circuit.id)

        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset

    @action(detail=True, methods=['get'], url_path='bins')
    def bins(self, request, pk=None):
        """Get all bins in a circuit."""
        from apps.bins.api.v1.serializers import BinListSerializer
        circuit = self.get_object()
        bins = circuit.bins.all()
        serializer = BinListSerializer(bins, many=True)
        return Response({
            'circuit': circuit.code,
            'total_bins': bins.count(),
            'bins': serializer.data
        })

    @action(detail=True, methods=['get'], url_path='stats')
    def stats(self, request, pk=None):
        """Get circuit statistics."""
        circuit = self.get_object()
        bins = circuit.bins.all()
        active_bins = bins.filter(status='active')
        online_bins = active_bins.filter(is_online=True)

        fill_levels = [b.fill_level for b in active_bins if b.fill_level is not None]
        avg_fill = round(sum(fill_levels) / len(fill_levels), 1) if fill_levels else 0
        critical_bins = [f for f in fill_levels if f >= 80]

        return Response({
            'circuit': circuit.code,
            'total_bins': bins.count(),
            'active_bins': active_bins.count(),
            'online_bins': online_bins.count(),
            'offline_bins': active_bins.count() - online_bins.count(),
            'average_fill_level': avg_fill,
            'critical_bins_count': len(critical_bins),
        })