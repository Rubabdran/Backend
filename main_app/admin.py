#----------managing backend data----------#

from django.contrib import admin
from .models import Image,Favorite,Comment

admin.site.register(Image)
admin.site.register(Favorite)
admin.site.register(Comment)