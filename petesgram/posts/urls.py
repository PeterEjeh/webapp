from django import views
from django.urls import path
from .views import feed
from . import views

urlpatterns = [
    path('', feed, name='feed'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
]
