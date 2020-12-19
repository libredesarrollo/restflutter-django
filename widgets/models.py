"""from widgets.models import Button, Behavior
b = Button.objects.get(pk=1) 
be = Behavior(content_object=b, content_1="Hola",content_2="Test", behavioral_model='content')
c = ContentType.objects.get_for_model(b) 
Behavior.objects.filter(button__id=1).first()
"""



from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

from stdimage import JPEGField

# Create your models here.

class Behavior(models.Model):

    TYPE = (
        ('url','Url'),
        ('resource','Resource'),
        ('content','Content'),
    )

    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()

    content_object = GenericForeignKey('content_type','object_id')

    content_1 = models.TextField()
    content_2 = models.TextField()
    behavioral_model = models.CharField(max_length=10, choices=TYPE, default='url')


class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Button(models.Model):

    TYPE =(
        ('flat', 'Flat'),
        ('raised', 'Raised'),
    )

    color = models.CharField(max_length=10)
    color_bg = models.CharField(max_length=10)
    label = models.CharField(max_length=255)
    icon = models.CharField(max_length=20)
    type = models.CharField(max_length=10,choices=TYPE, default='flat')
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    behavior = GenericRelation(Behavior, related_query_name="button")

    def __str__(self):
        return self.label

class Image(models.Model):
    name = models.CharField(max_length=255)
    url = JPEGField(upload_to='images/',variations={'custom':{'width':500, 'height':250,'crop':True}}) #models.CharField(max_length=200)
    
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    behavior = GenericRelation(Behavior, related_query_name="image")

    def __str__(self):
        return self.name

class Chip(models.Model):
    color = models.CharField(max_length=10)
    color_bg = models.CharField(max_length=10)
    label = models.CharField(max_length=255)
    icon = models.CharField(max_length=20)

    behavior = GenericRelation(Behavior, related_query_name="chip")

    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.label

class Text(models.Model):
    text = models.CharField(max_length=2000)

    #behavior = GenericRelation(Behavior, related_query_name="text")

    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return "{0}".format(self.id)

class Mix(models.Model):
    widget = models.CharField(max_length=10)
    widget_id = models.IntegerField()
    orden = models.IntegerField()
    
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return "{0}, {1} - {2}".format(self.widget, self.widget_id,self.group)

class Note(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    
    def __str__(self):
        return "{0}".format(self.title)