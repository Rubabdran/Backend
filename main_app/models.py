#----------- create tables in the database----------#

from django.db import models
from django.contrib.auth.models import User #built-in User model

#----------------- defines models ------------------#

#Image model representing user-generated images | one to many relationship
class Image(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE) #on_delete > if the user is deleted, all their images are deleted 
    prompt = models.TextField()
    image_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)  

    def __str__(self):
        return self.prompt 

#Favorite model representing many to many relationship between users and images
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user', 'image') #Ensures a user cannot favorite the same image more than once

#Represents comments made by users on images | One user can write many comments & One image can have many comments
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments") #related_name allow to me to querying
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

