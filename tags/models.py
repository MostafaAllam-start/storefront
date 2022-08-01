from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
class Tag(models.Model):
    label = models.CharField(max_length=255)
    
    def __str__(self):
        return self.label


class TaggedItemManager(models.Manager):
    def get_for_product(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(object_type = obj_type)
        return TaggedItem.objects \
        .select_related('tag') \
        .filter(
            content_type = content_type,
            object_id = obj_id,
        )

class TaggedItem(models.Model):
    # adding our manager object
    objects = TaggedItemManager()
    #what tag applied to what object
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # To define a generic relationship:
    # Type of an object(product, video, article, etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # ID
    object_id = models.PositiveIntegerField()
    # Content Object 
    content_object = GenericForeignKey()

     
