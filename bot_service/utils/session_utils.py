from django.contrib.sessions.backends.cache import SessionStore
from telegram import Update


def get_session_store(update: Update) -> SessionStore:
    session_key = update.message.from_user['id']
    ss = SessionStore(session_key=str(session_key))
    if not ss.exists(str(session_key)):
        ss._set_session_key(str(session_key))
        ss.save(True)
    return ss
