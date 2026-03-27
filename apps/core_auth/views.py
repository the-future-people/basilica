from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


class BasilicaTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom token serializer that adds user role
    and device_id to the JWT payload.
    """

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        # Add role info to response
        data['user_id'] = str(user.id)
        data['username'] = user.username
        data['email'] = user.email
        data['is_staff'] = user.is_staff

        # Add role
        if hasattr(user, 'driver_profile'):
            data['role'] = 'driver'
            data['circuit_id'] = str(user.driver_profile.circuit.id) if user.driver_profile.circuit else None
        elif user.is_staff:
            data['role'] = 'admin'
        else:
            data['role'] = 'unknown'

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['is_staff'] = user.is_staff

        if hasattr(user, 'driver_profile'):
            token['role'] = 'driver'
            token['device_id'] = user.driver_profile.registered_device_id or ''
        else:
            token['role'] = 'admin'

        return token


class BasilicaTokenObtainPairView(TokenObtainPairView):
    serializer_class = BasilicaTokenObtainPairSerializer


class MeView(APIView):
    """Returns the current authenticated user's profile."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_staff': user.is_staff,
        }

        if hasattr(user, 'driver_profile'):
            driver = user.driver_profile
            data['role'] = 'driver'
            data['driver'] = {
                'id': str(driver.id),
                'phone_number': driver.phone_number,
                'status': driver.status,
                'is_on_trip': driver.is_on_trip,
                'circuit': str(driver.circuit.id) if driver.circuit else None,
            }
        elif user.is_staff:
            data['role'] = 'admin'
        else:
            data['role'] = 'unknown'

        return Response(data)