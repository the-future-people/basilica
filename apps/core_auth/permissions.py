from rest_framework.permissions import BasePermission


class IsSystemAdmin(BasePermission):
    """Full access — Basilica superadmins only."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class IsCircuitAdmin(BasePermission):
    """Access scoped to their own circuit only."""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return hasattr(request.user, 'circuit_admin_profile')


class IsDriver(BasePermission):
    """Driver access — trip and bin collection only."""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return hasattr(request.user, 'driver_profile')


class IsDriverOrCircuitAdmin(BasePermission):
    """Either a driver or a circuit admin."""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return (
            hasattr(request.user, 'driver_profile') or
            hasattr(request.user, 'circuit_admin_profile') or
            request.user.is_staff
        )


class IsOwnerDriver(BasePermission):
    """Driver can only access their own data."""
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        if hasattr(obj, 'driver'):
            return obj.driver.user == request.user
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return False