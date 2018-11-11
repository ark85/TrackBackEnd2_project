from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from .models import Comment

User = get_user_model()


def add_comment(obj, user, content):
    """Add comment to `obj`.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    comment, is_created = Comment.objects.get_or_create(
        content_type=obj_type, object_id=obj.id, user=user, content=content)
    return comment


def remove_like(obj, user, content):
    """Remove comment from `obj`.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    Comment.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user, content=content
    ).delete()