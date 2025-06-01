from rest_framework.exceptions import Throttled

class APIKeyMixin:

    """
    Mixin to:
    - Skip DRF throttling if API key is present.
    - Enforce custom quota on the API key.
    """
    # skip throttle for API key users, it's optional as the same thing is done in the throttling.py file
    def get_throttles(self):
        if hasattr(self.request, "api_key"):
            return []
        return super().get_throttles()
    
    def enforce_api_key_quota(self, request):
        api_key = getattr(request, "api_key", None)
        if api_key:
            if not api_key.has_quota():
                raise Throttled(detail="API key quota exceeded")
            api_key.increment_usage()
