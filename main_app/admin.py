from django.contrib import admin
from .models import Image,Favorite,Comment

# Register your models here.
admin.site.register(Image)
admin.site.register(Favorite)
admin.site.register(Comment)