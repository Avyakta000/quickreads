import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from django.urls import re_path
from blog.routing import websocket_urlpatterns  # Import your routing

# Set the environment variable and verify
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_blog.settings")
print("DJANGO_SETTINGS_MODULE:", os.environ.get("DJANGO_SETTINGS_MODULE"))

# Initialize Django setup
try:
    django.setup()
    print("Django setup completed successfully.")
except Exception as e:
    print("Error during django.setup():", e)
    raise

# Import modules only after django.setup()
try:
    from blog import consumers  # Ensure correct path here
    from .custom_auth_middleware import JWTAuthMiddleware
except ImportError as e:
    print("ImportError:", e)
    raise

# Define the ASGI application
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        JWTAuthMiddleware(
            URLRouter(websocket_urlpatterns)
        )
    ),
})
