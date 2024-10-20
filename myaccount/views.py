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
from django.conf import settings

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

def email_confirmation(request, key):
    return redirect(f"http://localhost:5173/dj-rest-auth/registration/account-confirm-email/{key}")

def reset_password_confirm(request, uid, token):
    return redirect(f"http://localhost:5173/reset/password/confirm/{uid}/{token}")