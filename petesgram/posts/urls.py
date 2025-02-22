from django import views
from django.urls import path
from .views import feed, post_detail, user_profile, get_post_link
from . import views

urlpatterns = [
    path('', feed, name='feed'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('profile/<str:username>/', user_profile, name='user_profile'),
    path('track-share/', views.track_share, name='track_share'),
    path('posts/share/<int:post_id>/', views.share_post, name='share_post'),
    path('get_post_link/<int:post_id>/', get_post_link, name='get_post_link'),

]
