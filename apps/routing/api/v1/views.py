from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.routing.models import Routeplan, RoutePlanStop
from apps.core_auth.permissions import IsSystemAdmin, IsDriverOrCircuitAdmin
from .serializers import RoutePlanSerializer, RoutePlanListSerializer


class RoutePlanViewSet(viewsets.ModelViewSet):
    queryset = Routeplan.objects.select_related('circuit', 'trip').all()

    def get_serializer_class(self):
        if self.action == 'list':
            return RoutePlanListSerializer
        return RoutePlanSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsSystemAdmin()]
        return [IsAuthenticated(), IsDriverOrCircuitAdmin()]

    def get_queryset(self):
        user = self.request.user
        queryset = Routeplan.objects.select_related('circuit', 'trip').all()

        # Drivers only see route plans for their circuit
        if hasattr(user, 'driver_profile') and not user.is_staff:
            queryset = queryset.filter(circuit=user.driver_profile.circuit)

        circuit_id = self.request.query_params.get('circuit')
        if circuit_id:
            queryset = queryset.filter(circuit=circuit_id)

        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        date_filter = self.request.query_params.get('date')
        if date_filter:
            queryset = queryset.filter(scheduled_for=date_filter)

        return queryset

    @action(detail=True, methods=['post'], url_path='dispatch',
            permission_classes=[IsAuthenticated, IsSystemAdmin])
    def dispatch(self, request, pk=None):
        """Dispatch a ready route plan to the driver."""
        from django.utils import timezone
        route_plan = self.get_object()

        if route_plan.status != Routeplan.Status.READY:
            return Response(
                {'error': 'Only ready route plans can be dispatched.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        route_plan.status = Routeplan.Status.DISPATCHED
        route_plan.dispatched_at = timezone.now()
        route_plan.save()

        return Response(RoutePlanSerializer(route_plan).data)