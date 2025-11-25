from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token
from django.utils import timezone
from datetime import timedelta

class ExpiringTokenAuthentication(TokenAuthentication):
    # Token will expire in 3 days
    expiry_time = timedelta(days=3)

    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed("Invalid token.")

        # Check expiry
        if timezone.now() > (token.created + self.expiry_time):
            raise AuthenticationFailed({
                "message": "Token has expired after 3 days. Please login again."
            })

        return (token.user, token)
