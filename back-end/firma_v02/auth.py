from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication

class IsFarmer(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='farmer').exists()

class CookieJWTAuthentication(JWTAuthentication):
    """
    Custom authentication class that checks the cookie for the access token.
    """
    def authenticate(self, request):
        # First, try to get the token from the Authorization header.
        header = self.get_header(request)
        if header is not None:
            raw_token = self.get_raw_token(header)
        else:
            # If the header is not set, try to get the token from the cookie.
            raw_token = request.COOKIES.get('access_token')
        if raw_token is None:
            return None
        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token