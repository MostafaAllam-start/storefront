from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
class Tag(models.Model):
    label = models.CharField(max_length=255)

class TaggedItem(models.Model):
    #what tag applied to what object
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # To define a generic relationship:
    # Type of an object(product, video, article, etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # ID
    object_id = models.PositiveIntegerField()
    # Content Object 
    content_object = GenericForeignKey()

     
