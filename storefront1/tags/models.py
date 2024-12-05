from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.

class TaggedItemManager(models.Manager):
    def get_tags_for(self,obj_type, obj_id):
        content_type=ContentType.objects.get_for_model(Product)
        queryset=TaggedItem.objects \
        .select_related('tag') \
        .filter(
            content_type=content_type,
            object_id=obj_id
        )
class Tag(models.Model):
    label=models.CharField(max_length=255)
    
    def __str__(self)-> str:
        return self.label
    
    
class TaggedItem(models.Model):
    #what tag applied to what object
    tag=models.ForeignKey(Tag, on_delete=models.CASCADE)
    #Type(product,Video,Article)
    #ID
    content_type=models.ForeignKey(ContentType, on_delete=models.CASCADE)  #to identify the type of  object that is tagged
    object_id=models.PositiveIntegerField() #references the particular object
    content_object=GenericForeignKey() #to read the actual object
    objects=TaggedItemManager()