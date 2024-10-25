# Create your views here.
from django.shortcuts import render, redirect
from django.http import JsonResponse

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

from allauth.account.utils import send_email_confirmation
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from django.conf import settings

from dj_rest_auth.views import LoginView
from dj_rest_auth.registration.views import RegisterView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.settings import api_settings as jwt_settings

class ResendVerificationEmailView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if not user.emailaddress_set.filter(verified=True).exists():
            send_email_confirmation(request, user)
            return Response({"detail": "Verification email sent."}, status=status.HTTP_200_OK)
        return Response({"detail": "Email already verified."}, status=status.HTTP_400_BAD_REQUEST)

class GoogleLogin(SocialLoginView): # if you want to use Authorization Code Grant, use this
    # permission_classes = [AllowAny]
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = settings.GOOGLE_CALLBACK_URL

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        refresh_token_expiration = timezone.now() + jwt_settings.REFRESH_TOKEN_LIFETIME
        
        # Convert to ISO 8601 format
        refresh_token_expiration_iso = refresh_token_expiration.isoformat()

        # Add the expiration time to the response data
        response.data['refresh_token_expiration'] = refresh_token_expiration_iso
        
        return response


def email_confirmation(request, key):
    return redirect(f"http://localhost:5173/dj-rest-auth/registration/account-confirm-email/{key}")

def reset_password_confirm(request, uid, token):
    return redirect(f"http://localhost:5173/reset/password/confirm/{uid}/{token}")



class CustomLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        print('working time')
        # Calculate the refresh token expiration time
        refresh_token_expiration = timezone.now() + jwt_settings.REFRESH_TOKEN_LIFETIME
        
        # Convert to ISO 8601 format
        refresh_token_expiration_iso = refresh_token_expiration.isoformat()

        # Add the expiration time to the response data
        response.data['refresh_token_expiration'] = refresh_token_expiration_iso
        print(refresh_token_expiration, refresh_token_expiration_iso, '_ and iso')
                
        return response

class CustomRegisterView(RegisterView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        # Get refresh token lifetime
        refresh_token_expiration = timezone.now() + jwt_settings.REFRESH_TOKEN_LIFETIME
        
        # Convert to ISO 8601 format
        refresh_token_expiration_iso = refresh_token_expiration.isoformat()

        # Add the expiration time to the response data
        response.data['refresh_token_expiration'] = refresh_token_expiration_iso
                
        return response

# from rest_framework_simplejwt.views import TokenRefreshView
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.exceptions import InvalidToken
# from rest_framework.response import Response
# from rest_framework import status

# class CustomTokenRefreshView(TokenRefreshView):
    # def post(self, request, *args, **kwargs):
    #     refresh_token = request.COOKIES.get('refresh')  # Get the refresh token from the cookies
    #     if not refresh_token:
    #         return Response({"detail": "Refresh token not found."}, status=status.HTTP_400_BAD_REQUEST)

    #     try:
    #         # Use the refresh token from the cookie to generate a new access token
    #         token = RefreshToken(refresh_token)
    #         access_token = token.access_token

    #         # Create a response and set the new access token in the cookie
    #         response = Response({
    #             # "access": str(access_token),
    #             "refresh_token_expiration": token.lifetime.total_seconds(),
    #         })

    #         # Optionally, update the access token cookie
    #         response.set_cookie(
    #             key='access_token',
    #             value=str(access_token),
    #             httponly=True,
    #             secure=True,  # Set to True in production
    #             samesite='Lax',
    #             max_age=access_token.lifetime.total_seconds(),
    #         )

    #         return response
    #     except InvalidToken:
    #         return Response({"detail": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)
