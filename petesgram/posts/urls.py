from django.urls import path
from .views import feed, create_post, like_post, comment_post

urlpatterns = [
    path('', feed, name='feed'),
    path('new/', create_post, name='create_post'),
    path('like/<int:post_id>/', like_post, name='like_post'),
    path('comment/<int:post_id>/', comment_post, name='comment_post'),
]
