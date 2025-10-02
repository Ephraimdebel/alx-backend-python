from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Message
from .utils import get_thread   # import recursive helper

@login_required
def delete_user(request):
    if request.method == "POST":
        user = request.user
        username = user.username
        user.delete()  # This will trigger the post_delete signal
        return HttpResponse(f"User '{username}' and related data deleted successfully.")
    return HttpResponse("Invalid request. Use POST to delete account.", status=400)
def conversation_view(request):
    # ✅ Fetch top-level messages with related user + prefetch replies
    messages = (
        Message.objects.filter(parent_message__isnull=True)
        .select_related("user")  # joins user in one query
        .prefetch_related("replies__user")  # prefetch replies + their users
    )

    return render(request, "messaging/conversation.html", {"messages": messages})

def threaded_conversation_view(request, message_id):
    # Optimize query with select_related and prefetch_related
    root_message = get_object_or_404(
        Message.objects.select_related("sender", "receiver").prefetch_related("replies"),
        id=message_id,
        sender=request.user  # ensure current user is the sender
    )

    conversation = get_thread(root_message)

    return render(request, "messaging/thread.html", {"conversation": conversation})

def unread_inbox_view(request):
    # ✅ Use the custom manager to fetch unread messages for logged-in user
    unread_messages = Message.unread.for_user(request.user)

    return render(request, "messaging/unread_inbox.html", {"unread_messages": unread_messages})