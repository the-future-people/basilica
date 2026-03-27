from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from apps.drivers.models import Driver, Trip, TripStop
from apps.core_auth.permissions import IsSystemAdmin, IsDriver, IsDriverOrCircuitAdmin, IsOwnerDriver
from .serializers import DriverSerializer, TripSerializer, TripListSerializer, TripStopSerializer


class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.select_related('user', 'circuit').all()
    serializer_class = DriverSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsSystemAdmin()]
        return [IsAuthenticated(), IsDriverOrCircuitAdmin()]

    def get_queryset(self):
        user = self.request.user
        queryset = Driver.objects.select_related('user', 'circuit').all()

        # Drivers can only see themselves
        if hasattr(user, 'driver_profile') and not user.is_staff:
            return queryset.filter(user=user)

        circuit_id = self.request.query_params.get('circuit')
        if circuit_id:
            queryset = queryset.filter(circuit=circuit_id)

        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset

    @action(detail=True, methods=['get'], url_path='trips')
    def trips(self, request, pk=None):
        """Get all trips for a driver."""
        driver = self.get_object()
        trips = Trip.objects.filter(driver=driver).order_by('-scheduled_date')
        serializer = TripListSerializer(trips, many=True)
        return Response(serializer.data)


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.select_related('driver', 'circuit').all()

    def get_serializer_class(self):
        if self.action == 'list':
            return TripListSerializer
        return TripSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsAuthenticated(), IsSystemAdmin()]
        return [IsAuthenticated(), IsDriverOrCircuitAdmin()]

    def get_queryset(self):
        user = self.request.user
        queryset = Trip.objects.select_related('driver', 'circuit').all()

        # Drivers only see their own trips
        if hasattr(user, 'driver_profile') and not user.is_staff:
            queryset = queryset.filter(driver=user.driver_profile)

        circuit_id = self.request.query_params.get('circuit')
        if circuit_id:
            queryset = queryset.filter(circuit=circuit_id)

        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        date_filter = self.request.query_params.get('date')
        if date_filter:
            queryset = queryset.filter(scheduled_date=date_filter)

        return queryset

    @action(detail=True, methods=['post'], url_path='start')
    def start_trip(self, request, pk=None):
        """Driver toggles to start their trip."""
        trip = self.get_object()

        if trip.status != Trip.Status.PENDING:
            return Response(
                {'error': 'Only pending trips can be started.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Make sure it's the assigned driver
        if hasattr(request.user, 'driver_profile'):
            if trip.driver != request.user.driver_profile:
                return Response(
                    {'error': 'You are not assigned to this trip.'},
                    status=status.HTTP_403_FORBIDDEN
                )

        trip.status = Trip.Status.IN_PROGRESS
        trip.started_at = timezone.now()
        trip.save()

        # Mark driver as on trip
        trip.driver.is_on_trip = True
        trip.driver.save()

        return Response(TripSerializer(trip).data)

    @action(detail=True, methods=['post'], url_path='complete')
    def complete_trip(self, request, pk=None):
        """Driver completes their trip."""
        trip = self.get_object()

        if trip.status != Trip.Status.IN_PROGRESS:
            return Response(
                {'error': 'Only in-progress trips can be completed.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        trip.status = Trip.Status.COMPLETED
        trip.completed_at = timezone.now()
        trip.total_bins_collected = trip.stops.filter(
            status=TripStop.Status.COLLECTED
        ).count()
        trip.save()

        # Mark driver as off trip
        trip.driver.is_on_trip = False
        trip.driver.last_active_at = timezone.now()
        trip.driver.save()

        return Response(TripSerializer(trip).data)

    @action(detail=True, methods=['post'], url_path='stops/(?P<stop_id>[^/.]+)/collect')
    def collect_stop(self, request, pk=None, stop_id=None):
        """Mark a specific bin stop as collected."""
        trip = self.get_object()

        try:
            stop = trip.stops.get(id=stop_id)
        except TripStop.DoesNotExist:
            return Response(
                {'error': 'Stop not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        stop.status = TripStop.Status.COLLECTED
        stop.collected_at = timezone.now()
        stop.notes = request.data.get('notes', '')
        stop.save()

        return Response(TripStopSerializer(stop).data)

    @action(detail=True, methods=['post'], url_path='stops/(?P<stop_id>[^/.]+)/skip')
    def skip_stop(self, request, pk=None, stop_id=None):
        """Mark a specific bin stop as skipped."""
        trip = self.get_object()

        try:
            stop = trip.stops.get(id=stop_id)
        except TripStop.DoesNotExist:
            return Response(
                {'error': 'Stop not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        stop.status = TripStop.Status.SKIPPED
        stop.notes = request.data.get('notes', '')
        stop.save()

        return Response(TripStopSerializer(stop).data)