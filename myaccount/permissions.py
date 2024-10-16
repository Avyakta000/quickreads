from rest_framework import permissions

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

