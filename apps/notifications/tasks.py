from celery import shared_task

from .services import create_notification


@shared_task
def send_notification(
    user_id,
    notification_type,
    title,
    message,
):
    from apps.accounts.models import User

    user = User.objects.get(id=user_id)

    notification = create_notification(
        user=user,
        notification_type=notification_type,
        title=title,
        message=message,
    )

    return notification.id