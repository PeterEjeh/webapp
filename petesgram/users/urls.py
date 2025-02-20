from django import views
from django.urls import path
from .views import delete_post, register, profile, profile_view, edit_profile
from posts.views import upload
from django.contrib.auth import views as auth_views
from .views import (
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView
)



urlpatterns = [
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  
    path('profile/<str:username>/', profile_view, name='profile'),  
    path('profile/', profile, name='profile'),
    path("edit-profile/", edit_profile, name="edit_profile"),
    path("upload/", upload, name="upload"),
    path('post/delete/<int:post_id>/', delete_post, name='delete_post'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
