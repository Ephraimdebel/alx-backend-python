# Django-Middleware-0x03/chats/middleware.py
import logging
import os
from datetime import datetime
from django.conf import settings

# Setup logger once (avoid duplicate handlers on reload)
logger = logging.getLogger("chats.request_logger")
if not logger.handlers:
    # ensure BASE_DIR exists in settings; fallback to cwd
    base = getattr(settings, "BASE_DIR", os.getcwd())
    log_file = os.path.join(base, "requests.log")
    handler = logging.FileHandler(log_file)
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


class RequestLoggingMiddleware:
    """
    Middleware that logs each request with timestamp, user, and path.
    Writes lines like:
        2025-09-28 12:34:56.789123 - User: ephraim - Path: /api/conversations/
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Determine username (use 'Anonymous' if not authenticated)
        user = "Anonymous"
        try:
            if hasattr(request, "user") and request.user.is_authenticated:
                # prefer username if available
                user = getattr(request.user, "username", str(request.user))
        except Exception:
            # in some early request phases request.user may not exist
            user = "Anonymous"

        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)

        response = self.get_response(request)
        return response
