from django.contrib import admin
from .models import Subscriber, Tag, TableOfContent, BlogPost
# Register your models here.

admin.site.register(Subscriber) 
admin.site.register(Tag)
admin.site.register(TableOfContent)
admin.site.register(BlogPost)


