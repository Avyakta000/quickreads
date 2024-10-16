from django.urls import path, include
from .views import  GoogleLogin, email_confirmation, reset_password_confirm, ResendVerificationEmailView
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
   
    # path('auth/', include('dj_rest_auth.urls')),
    # path('auth/jwt/obtain/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('auth/jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('rest-auth/registration/', include('dj_rest_auth.registration.urls')),

    path('', include('allauth.urls')),
    path('rest-auth/', include('dj_rest_auth.urls')),
    path('resend-verification-email/', ResendVerificationEmailView.as_view(), name='resend-verification-email'),
    path('dj-rest-auth/registration/account-confirm-email/<str:key>/', email_confirmation),
    path('reset/password/confirm/<int:uid>/<str:token>', reset_password_confirm, name="password_reset_confirm"),
    path('rest-auth/google/', GoogleLogin.as_view(), name='google_login'),
   
]