from django.urls import path
from . import views

urlpatterns = [
  path('', views.Home.as_view(), name='home'),
  path('users/signup/', views.CreateUserView.as_view(), name='signup'),
  path('users/login/', views.LoginView.as_view(), name='login'),
  path('users/token/refresh/', views.VerifyUserView.as_view(), name='token_refresh'),
  path('images/', views.CreateImage.as_view(), name='image-list-create'),
  
  path('images/<int:pk>/publish/', views.PublishImageView.as_view(), name='image-publish'),
  path('images/<int:pk>/favorite/', views.ToggleFavoriteView.as_view(), name='image-favorite'),
  
  path('images/explore/', views.ExplorePublicImagesView.as_view(), name='explore-public-images'),
  path('images/favorites/', views.ListFavoriteImagesView.as_view(), name='all-favorites-images'),


]