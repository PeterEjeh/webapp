from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from posts.models import Post  # Assuming 'Post' is the model for user posts
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .models import Profile  # Import UserProfile model
from django.contrib import messages
from django.http import JsonResponse






def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')


# Profile Page View
from users.models import Profile  # Import Profile model

@login_required
@login_required
def profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user_profile).order_by('-created_at')

    is_following = request.user in user_profile.profile.followers.all()

    context = {
        'profile': user_profile.profile,
        'user_profile': user_profile,
        'posts': posts,
        'post_count': posts.count(),
        'is_following': is_following,
    }
    return render(request, 'users/profile.html', context)




# Follow/Unfollow User
@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)

    # Ensure profile exists or create one
    profile, created = Profile.objects.get_or_create(user=user_to_follow)

    is_following = False  # Default state

    if request.user in profile.followers.all():
        profile.followers.remove(request.user)  # Unfollow
    else:
        profile.followers.add(request.user)  # Follow
        is_following = True  # Update state

    # Return JSON response for AJAX
    return JsonResponse({'is_following': is_following})

# Upload Post View
@login_required
def upload_post(request):
    if request.method == 'POST' and request.FILES.get('media'):
        media_file = request.FILES['media']
        caption = request.POST.get('caption', '')  # Get caption from form

        new_post = Post(
            user=request.user,
            caption=caption,  # Add the caption
            image=media_file if media_file.content_type.startswith('image') else None,
            video=media_file if media_file.content_type.startswith('video') else None
        )
        new_post.save()
        return redirect('profile', username=request.user.username)

    return render(request, 'posts/upload.html')
class CustomLoginView(LoginView):
    template_name = "users/login.html"

def edit_profile(request):
    return render(request, 'users/edit_profile.html')

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.user == request.user:  # Ensure the user owns the post
        post.delete()
        messages.success(request, "Post deleted successfully!")
    else:
        messages.error(request, "You are not allowed to delete this post!")

    return redirect('profile', username=request.user.username)