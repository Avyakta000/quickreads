from myaccount.models import ApplicationAPIKey
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class ApplicationAPIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Api-Key "):
            print("No API key provided")
            return None

        key = auth.split(" ")[1]
        try:
            api_key = ApplicationAPIKey.objects.get_from_key(key)
            print("API key found")
        except ApplicationAPIKey.DoesNotExist:
            raise AuthenticationFailed("Invalid API key")
        if not api_key.is_active:
            raise AuthenticationFailed("API key is disabled")
        
        # set api_key in the request object as custom attribute (to access api_key obj we can use request.auth) to be used in the throttling.py file and the mixins.py file
        request.api_key = api_key
        # return None, None to bypass the authentication
        return (api_key.associated_user, api_key)