from pyrogram.types import User

def mention_user(user: User) -> str:
    """Return a clickable mention for a user"""
    if user.username:
        return f"@{user.username}"
    return f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"
