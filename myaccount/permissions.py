from rest_framework import permissions
from rest_framework_api_key.permissions import BaseHasAPIKey
from myaccount.models import ApplicationAPIKey
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class IsEmailVerified(permissions.BasePermission):
    """
    Custom permission to only allow users with verified emails to access certain views.
    """

    def has_permission(self, request, view):
        # Allow unrestricted access if the user is not authenticated
        if request.user and request.user.is_authenticated:
            # Check if the user's email is verified
            return request.user.emailaddress_set.filter(verified=True).exists()
        return False  # Deny permission if user is not authenticated or email is not verified

# API Key Permission, it's not used in the project
class HasApplicationAPIKey(BaseHasAPIKey):
    model = ApplicationAPIKey
    DEFAULT_API_KEY_HEADER_NAME = "Api-Key"

    def get_key(self, request):
        auth = request.headers.get("Authorization")
        if not auth:
            return None

        parts = auth.split()

        if len(parts) == 2 and parts[0] == self.DEFAULT_API_KEY_HEADER_NAME:
            return parts[1]

        return None

    def has_permission(self, request, view):
        key = self.get_key(request)
        if not key:
            return False

        try:
            api_key = self.model.objects.get_from_key(key)
        except self.model.DoesNotExist:
            return False

        if not (api_key.is_valid and api_key.has_quota()):
            return False

        api_key.increment_usage()
        return True
    
