def get_thread(message):
    """
    Recursively fetch all replies for a given message.
    """
    thread = {
        "message": message,
        "replies": []
    }
    for reply in message.replies.all().select_related("user"):
        thread["replies"].append(get_thread(reply))
    return thread
