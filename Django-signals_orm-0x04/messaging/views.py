from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def delete_user(request):
    if request.method == "POST":
        user = request.user
        username = user.username
        user.delete()  # This will trigger the post_delete signal
        return HttpResponse(f"User '{username}' and related data deleted successfully.")
    return HttpResponse("Invalid request. Use POST to delete account.", status=400)
