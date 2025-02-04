from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from datetime import datetime
from django.utils import timezone
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from models_only.models import Farmer

        
USER_TYPES = {
    'FARMER': 'farmer',
    'SEARCHER': 'searcher',
    'POLICY_MAKER': 'policy_maker'
}

class FARMERJWTAuthentication(JWTAuthentication):

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        try:
            token = AccessToken(raw_token)
            payload = token.payload

            # Validate token expiration
            exp = payload.get('exp')
            if exp and datetime.fromtimestamp(exp) < datetime.now():
                raise AuthenticationFailed("Token has expired")

            # Validate required payload fields
            user_id = payload.get('user_id')
            user_type = payload.get('user_type')
            if not user_id or not user_type:
                raise AuthenticationFailed("Invalid token payload")

            # Ensure only farmers can access this view
            if user_type != USER_TYPES['FARMER']:
                raise AuthenticationFailed("Only farmers are allowed to access this resource.")

            # Fetch the farmer user
            try:
                user = Farmer.objects.get(id=user_id)
                user.is_authenticated = True
                return (user, token)
            except Farmer.DoesNotExist:
                raise AuthenticationFailed("Farmer does not exist")

        except TokenError:
            raise AuthenticationFailed("Invalid token")