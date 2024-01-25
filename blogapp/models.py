from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from cloudinary.models import CloudinaryField

class Subscriber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscribe = models.BooleanField(default=True)
    # profile_pic = models.ImageField(null=True, blank=True, default = 'default.webp')
    profile_pic = CloudinaryField('image', null=True, blank=True)

    def __str__(self):
        return self.user.username + " " + str(self.subscribe)

class Tag(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)    

    class Meta:
        verbose_name_plural = 'Tags'

    def __str__(self):
        return str(self.name)

    
class TableOfContent(models.Model):
    content = models.CharField(max_length=200, blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True,blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Table of Contents'

    def __str__(self):
        return str(self.content)
    

class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    intro = models.TextField(blank = True, )
    tags = models.ManyToManyField('Tag', blank=True)
    content = models.TextField()
    publish_date = models.DateField(blank=True, null=True)
    slug = models.SlugField(max_length=150, unique=True)
    last_update = models.DateField(blank=True, null=True)
    toc = models.ManyToManyField('TableOfContent', blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.title)

