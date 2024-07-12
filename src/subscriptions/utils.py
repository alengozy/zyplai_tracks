from src.db.models import Track


def send_email_notification(track: Track, user_email: str):
    print(f"A new song titled {track.title} was released!")