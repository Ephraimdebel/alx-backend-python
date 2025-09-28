# Django-Middleware-0x03/chats/middleware.py
import logging
import os
from datetime import datetime
from django.conf import settings
from datetime import datetime
from django.http import HttpResponseForbidden
# Django-Middleware-0x03/chats/middleware.py
from django.http import HttpResponseForbidden
import time
from django.http import JsonResponse

# Setup logger once (avoid duplicate handlers on reload)
logger = logging.getLogger("chats.request_logger")
if not logger.handlers:
    # ensure BASE_DIR exists in settings; fallback to cwd
    base = getattr(settings, "BASE_DIR", os.getcwd())
    log_file = os.path.join(settings.BASE_DIR.parent, "requests.log")
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

class RestrictAccessByTimeMiddleware:
    """
    Middleware to restrict access to chat outside 6AM - 9PM.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define allowed hours: 6:00 to 21:00
        current_hour = datetime.now().hour
        if current_hour < 6 or current_hour >= 21:
            return HttpResponseForbidden(
                "Access to the chat is restricted between 9PM and 6AM."
            )

        response = self.get_response(request)
        return response

class OffensiveLanguageMiddleware:
    """
    Middleware to limit number of POST requests (messages) from a single IP.
    Each IP can only send 5 messages per minute. Excess requests get HTTP 429.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # Dictionary to track IP request times
        # Format: { "ip_address": [timestamp1, timestamp2, ...] }
        self.ip_request_log = {}

    def __call__(self, request):
        # Only track POST requests to messaging endpoints
        if request.method == "POST" and "messages" in request.path:
            ip = self.get_client_ip(request)
            now = time.time()

            if ip not in self.ip_request_log:
                self.ip_request_log[ip] = []

            # Remove timestamps older than 1 minute
            self.ip_request_log[ip] = [
                t for t in self.ip_request_log[ip] if now - t < 60
            ]

            # Check if limit exceeded
            if len(self.ip_request_log[ip]) >= 5:
                return JsonResponse(
                    {"detail": "Message limit exceeded. Please wait before sending more."},
                    status=429
                )

            # Log current request
            self.ip_request_log[ip].append(now)

        response = self.get_response(request)
        return response

    @staticmethod
    def get_client_ip(request):
        """Retrieve client IP address from request headers"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR", "")
        return ip

class RolepermissionMiddleware:
    """
    Middleware that restricts access to certain actions based on user role.
    Only users with role 'admin' or 'moderator' can proceed.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only enforce for authenticated users
        if hasattr(request, "user") and request.user.is_authenticated:
            # Assuming your User model has a 'role' attribute
            role = getattr(request.user, "role", None)
            if role not in ["admin", "moderator"]:
                return HttpResponseForbidden("You do not have permission to access this resource.")
        else:
            # Anonymous users are blocked
            return HttpResponseForbidden("You must be logged in to access this resource.")

        response = self.get_response(request)
        return response
