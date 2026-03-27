from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from apps.drivers.models import Driver


class BasilicaJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication that:
    - Validates the token
    - Checks device binding for drivers
    - Checks if user is active
    """

    def get_user(self, validated_token):
        user = super().get_user(validated_token)

        # Check user is active
        if not user.is_active:
            raise AuthenticationFailed('User account is disabled.')

        # Device binding check for drivers
        try:
            driver = user.driver_profile
            device_id = validated_token.get('device_id')

            if driver.registered_device_id and device_id != driver.registered_device_id:
                raise AuthenticationFailed('Unrecognized device. Access denied.')

        except Driver.DoesNotExist:
            pass

        return user