from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.bins.models import Bin, BinTelemetry
from apps.core_auth.permissions import IsSystemAdmin, IsCircuitAdmin, IsDriverOrCircuitAdmin
from .serializers import BinSerializer, BinListSerializer, BinTelemetrySerializer


class BinViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsDriverOrCircuitAdmin]
    queryset = Bin.objects.select_related('circuit').all()

    def get_serializer_class(self):
        if self.action == 'list':
            return BinListSerializer
        return BinSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Bin.objects.select_related('circuit').all()

        # Drivers only see bins in their circuit
        if hasattr(user, 'driver_profile') and not user.is_staff:
            queryset = queryset.filter(circuit=user.driver_profile.circuit)

        # Filter by circuit if provided
        circuit_id = self.request.query_params.get('circuit')
        if circuit_id:
            queryset = queryset.filter(circuit=circuit_id)

        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # Filter by fill level threshold
        fill_threshold = self.request.query_params.get('fill_above')
        if fill_threshold:
            bin_ids = [
                b.id for b in queryset
                if b.fill_level is not None and b.fill_level >= int(fill_threshold)
            ]
            queryset = queryset.filter(id__in=bin_ids)

        return queryset

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsSystemAdmin()]
        return [IsAuthenticated(), IsDriverOrCircuitAdmin()]

    @action(detail=True, methods=['get'], url_path='telemetry')
    def telemetry(self, request, pk=None):
        """Get telemetry history for a specific bin."""
        bin_obj = self.get_object()
        limit = int(request.query_params.get('limit', 50))
        telemetry = BinTelemetry.objects.filter(bin=bin_obj).order_by('-recorded_at')[:limit]
        serializer = BinTelemetrySerializer(telemetry, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='toggle-status',
            permission_classes=[IsAuthenticated, IsSystemAdmin])
    def toggle_status(self, request, pk=None):
        """Activate or deactivate a bin."""
        bin_obj = self.get_object()
        new_status = request.data.get('status')
        if new_status not in dict(Bin.Status.choices):
            return Response(
                {'error': 'Invalid status.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        bin_obj.status = new_status
        bin_obj.save()
        return Response(BinSerializer(bin_obj).data)

    @action(detail=False, methods=['get'], url_path='critical')
    def critical(self, request):
        """Return all bins above 80% fill level — needs urgent collection."""
        queryset = self.get_queryset()
        critical_bins = [b for b in queryset if b.fill_level is not None and b.fill_level >= 80]
        serializer = BinListSerializer(critical_bins, many=True)
        return Response({
            'count': len(critical_bins),
            'bins': serializer.data
        })

    @action(detail=False, methods=['get'], url_path='offline')
    def offline(self, request):
        """Return all bins that are currently offline."""
        queryset = self.get_queryset().filter(is_online=False, status='active')
        serializer = BinListSerializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'bins': serializer.data
        })