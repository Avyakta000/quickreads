from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class CustomAnonThrottle(AnonRateThrottle):
    def allow_request(self, request, view):
        api_key = getattr(request, "api_key", None)
        # Skip throttling if rate limit not applied for this key
        if api_key and not api_key.apply_rate_limit:
                return True
        return super().allow_request(request, view)

class CustomUserThrottle(UserRateThrottle):
    def allow_request(self, request, view):
        api_key = getattr(request, "api_key", None)
        # Skip throttling if rate limit not applied for this key
        if api_key and not api_key.apply_rate_limit:
                return True
        return super().allow_request(request, view)

