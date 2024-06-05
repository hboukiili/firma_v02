from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from datetime import datetime
from django.utils import timezone
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from models_only.models import Farmer


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
            exp = token.payload.get('exp')
            user_id = token.payload.get('user_id')
            user_type = token.payload.get('user_type')

            if datetime.fromtimestamp(exp) < datetime.now():
                raise AuthenticationFailed("Token has expired")

            if user_type == 'farmer':
    
                try:
    
                    user = Farmer.objects.get(id=user_id)
                    user.is_authenticated = True
                    return (user, token)

                except Farmer.DoesNotExist:
                    raise AuthenticationFailed("Farmer does not exist")
            else:

                if user_type == 'searcher' or user_type == 'policy_maker':
                    raise AuthenticationFailed("Do not have have right to access this page")
                raise AuthenticationFailed("Invalid user type")
    
        except TokenError as e:
            raise AuthenticationFailed("Token has expired")