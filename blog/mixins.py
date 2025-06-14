from rest_framework.exceptions import Throttled

class APIKeyMixin:

    """
    Mixin to:
    - Skip DRF throttling if API key is present.
    - Enforce custom quota on the API key.
    """
    # skip throttle for API key users, it's optional as the same thing is done in the throttling.py file
    def get_throttles(self):
        api_key = getattr(self.request, "api_key", None)
        print("api_key get_throttles", api_key)
        # Skip DRF throttling if API key present and apply_rate_limit is False
        if api_key and not api_key.apply_rate_limit:
            return []
        return super().get_throttles()
    
    def enforce_api_key_quota(self, request):
        api_key = getattr(request, "api_key", None)
        print(api_key)
        if api_key:
            print("api_key.has_quota()", api_key.has_quota())
            if not api_key.has_quota():
                raise Throttled(detail="API key quota exceeded")
            # increment usage only if quota allows
            if not api_key.increment_usage():
                raise Throttled(detail="API key usage limit exceeded")
