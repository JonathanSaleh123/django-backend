from rest_framework import authentication, exceptions
from django.contrib.auth.models import User
from checklist.utils import jwt_decode_token

class Auth0JSONWebTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth = request.headers.get('Authorization', None)
        if not auth:
            return None

        parts = auth.split()
        if parts[0].lower() != 'bearer' or len(parts) != 2:
            raise exceptions.AuthenticationFailed('Invalid Authorization header')

        token = parts[1]

        try:
            payload = jwt_decode_token(token)
        except Exception as e:
            raise exceptions.AuthenticationFailed(f'JWT decode failed: {str(e)}')

        user_id = payload.get('sub')
        if not user_id:
            raise exceptions.AuthenticationFailed('Missing subject (sub) claim in JWT')

        user, created = User.objects.get_or_create(username=user_id)
        if created or not user.is_active:
            user.is_active = True
            user.save()
        # print(f"Authenticated user: {user.username} ")
        return (user, token)
