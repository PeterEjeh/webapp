from django.urls import path
from . import views  # Import views from users
from .views import CustomLoginView, follow_user, upload_post, edit_profile, delete_post
from django.shortcuts import redirect


def profile_redirect(request):
    return redirect(f"/profile/{request.user.username}/")

urlpatterns = [
    path('register/', views.register, name='register'),  # User registration
    path("login/", CustomLoginView.as_view(), name="login"),
    path('logout/', views.user_logout, name='logout'),  # Logout function
    path('profile/<str:username>/', views.profile, name='profile'),
    path("accounts/profile/", profile_redirect),
    path('profile/<str:username>/follow/', follow_user, name='follow'),
    path('upload/', upload_post, name='upload'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('delete_post/<int:post_id>/', delete_post, name='delete_post'),

]
