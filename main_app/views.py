#---------------all API endpoints--------------#

from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from django.contrib.auth.models import User
from .serializers import UserSerializer, ImageSerializer, FavoriteSerializer, CommentSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import Image, Favorite,  Comment
from django.shortcuts import get_object_or_404

#----------------------classes---------------------#

#simple test route for checking if the API is running
class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to - api home route!'}
    return Response(content)
  
#--------------- user authentication----------------#

#user registration
class CreateUserView(generics.CreateAPIView):
  print("hello")
  queryset = User.objects.all()
  serializer_class = UserSerializer
  def create(self, request, *args, **kwargs):
    try:
      response = super().create(request, *args, **kwargs)
      user = User.objects.get(username=response.data['username'])
      refresh = RefreshToken.for_user(user)
      content = {'refresh': str(refresh), 'access': str(refresh.access_token), 'user': response.data }
      return Response(content, status=status.HTTP_200_OK)
    except (ValidationError, IntegrityError) as err:
      print(err)
      return Response({ 'error': str(err)}, status=status.HTTP_400_BAD_REQUEST)


#user login
class LoginView(APIView):

    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(username=username, password=password)
            
            if user:
                refresh = RefreshToken.for_user(user)
                content = {
                    'access': str(refresh.access_token),
                    'user': UserSerializer(user).data
                }
                return Response(content, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
                
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#Checks if the current access token is valid         
class VerifyUserView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    try:
      user = User.objects.get(username=request.user.username)
      try:
        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh),'access': str(refresh.access_token),'user': UserSerializer(user).data}, status=status.HTTP_200_OK)
      except Exception as token_error:
        return Response({"detail": "Failed to generate token.", "error": str(token_error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as err:
      return Response({"detail": "Unexpected error occurred.", "error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#------------------image creation---------------------#

#users can generate and save an image      
class CreateImage(APIView):
  serializer_class = ImageSerializer
  permission_classes = [permissions.IsAuthenticated]
  
  def post(self, request):
    print(request.data)
    try:
      serializer = self.serializer_class(data=request.data)
      if serializer.is_valid():
        serializer.save(owner=self.request.user)
        return Response(serializer.data, status=200)
      print(serializer.errors)
      return Response(serializer.errors, status=400)
    except Exception as err:
      return Response({'error':str(err)}, status=400)
  
#adds/removes an image from the user's favorites         
class ToggleFavoriteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            image = get_object_or_404(Image, pk=pk)
            favorite, created = Favorite.objects.get_or_create(user=request.user, image=image)

            if not created:
                favorite.delete()
                return Response({'status': 'Removed from favorites'}, status=200)
            return Response({'status': 'Added to favorites'}, status=200)
        except Exception as err:
            return Response({'error': str(err)}, status=400)

#returns all favorited images by the authenticated user.
class ListFavoriteImagesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            favorites = Favorite.objects.filter(user=request.user).select_related('image')
            images = [favorite.image for favorite in favorites]
            serializer = ImageSerializer(images, many=True)
            return Response(serializer.data, status=200)
        except Exception as err:
            return Response({'error': str(err)}, status=400)

#removes a specific image from favorites
class DeleteFavoriteImageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            favorite = Favorite.objects.filter(user=request.user, image__id=pk).first()
            if favorite:
                favorite.delete()
                return Response({'status': 'Deleted'}, status=status.HTTP_204_NO_CONTENT)
            return Response({"detail": "Favorite not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


#-----------------puplishing & exploration-------------# 

#allows a user to make their image public.        
class PublishImageView(APIView):
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        try:
            image = get_object_or_404(Image, pk=pk, owner=request.user)
            image.is_public = True
            image.save()
            serializer = self.serializer_class(image)
            return Response(serializer.data, status=200)
        except Exception as err:
            return Response({'error': str(err)}, status=400)
        
#lists all public images, available to any user.
class ExplorePublicImagesView(generics.ListAPIView):
    queryset = Image.objects.filter(is_public=True)
    serializer_class = ImageSerializer
    permission_classes = [permissions.AllowAny]

#---------------------comments----------------------#

#adds a comment (emoji) to a specific image.
class CreateCommentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, image_id):
        try:
            image = get_object_or_404(Image, id=image_id)
            emoji = request.data.get("emoji")

            if not emoji:
                return Response({"error": "Emoji is required"}, status=400)

            comment = Comment.objects.create(user=request.user, image=image, text=emoji)
            return Response(CommentSerializer(comment).data, status=201)
        except Exception as err:
            return Response({'error': str(err)}, status=400)