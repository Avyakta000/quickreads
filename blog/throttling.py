from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class CustomAnonThrottle(AnonRateThrottle):
    def allow_request(self, request, view):
        # skip throttle for API key users
        if hasattr(request, "api_key"):
            print("bypassing throttle")
            return True  
        return super().allow_request(request, view)

class CustomUserThrottle(UserRateThrottle):
    def allow_request(self, request, view):
        # skip throttle for API key users
        if hasattr(request, "api_key"):
            print("bypassing user throttle")
            return True  
        return super().allow_request(request, view)
