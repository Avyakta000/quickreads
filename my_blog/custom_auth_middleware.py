# custom_auth_middleware.py

from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth import get_user_model
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
import jwt
from django.conf import settings

User = get_user_model()

@database_sync_to_async
def get_user_from_token(token):
    """
    Retrieve the user associated with the token.
    """
    try:
        payload = UntypedToken(token)
        user_id = payload["user_id"]
        return User.objects.get(id=user_id)
    except (User.DoesNotExist, TokenError, InvalidToken):
        return AnonymousUser()

class JWTAuthMiddleware:
    """
    Custom middleware that extracts JWT from WebSocket cookies,
    validates it, and attaches the user to the scope.
    """
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        # First, authenticate the user
        scope = await self.authenticate(scope)

        # Now call the inner application
        return await self.inner(scope, receive, send)

    async def authenticate(self, scope):
        headers = dict(scope["headers"])
        
        # Get JWT from cookies in headers
        if b"cookie" in headers:
            cookies = headers[b"cookie"].decode()
            access_token = None
            for cookie in cookies.split("; "):
                if cookie.startswith("access="):
                    access_token = cookie.split("=")[1]
                    break
            
            if access_token:
                scope["user"] = await get_user_from_token(access_token)
            else:
                scope["user"] = AnonymousUser()
        else:
            scope["user"] = AnonymousUser()
        
        return scope
