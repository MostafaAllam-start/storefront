from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # GenericRelationship:
    # Object Types
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # Object ID
    object_id = models.PositiveIntegerField()
    # Content object
    content_object = GenericForeignKey()

