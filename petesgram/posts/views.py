from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import Share

from .models import Post, Like, Comment
from .forms import PostForm  
from .models import Post

def feed(request):
    posts = Post.objects.all().order_by('-created_at')  # Fetch posts, newest first
    return render(request, "posts/feed.html", {"posts": posts})

@login_required
def upload(request):
    if request.method == 'POST':
        # Get the uploaded files and caption from the request
        image = request.FILES.get('image')
        video = request.FILES.get('video')
        caption = request.POST.get('caption')

        # Validate that either an image or video is uploaded
        if not image and not video:
            return render(request, 'posts/upload.html', {'error': 'Please upload an image or video.'})

        # Create a new Post instance
        post = Post(
            user=request.user,
            image=image,
            video=video,
            caption=caption
        )
        post.save()

        return redirect('profile', username=request.user.username)  # Redirect to the user's profile
    else:
        return render(request, 'posts/upload.html')
    

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if not created:  # If like exists, remove it (toggle)
        like.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'likes_count': post.likes_count})
    return redirect('feed')

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        text = request.POST.get('comment_text')
        if text:
            Comment.objects.create(user=request.user, post=post, text=text)
    return redirect('feed')


@login_required
def follow_user(request, username):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    user_to_follow = get_object_or_404(User, username=username)
    is_following = user_to_follow in request.user.profile.following.all()

    if request.method == 'POST':
        if is_following:
            request.user.profile.following.remove(user_to_follow)
            status = 'unfollowed'
        else:
            request.user.profile.following.add(user_to_follow)
            status = 'followed'

        # Handle AJAX request (used in your template for dynamic updates)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': status})

        # Handle non-AJAX request (e.g., direct form submission)
        current_path = request.path
        if '/users/profile/' in current_path and username in current_path:
            # If on a profile page, redirect back to the same profile
            return redirect('users:profile', username=username)
        else:
            # If on the feed or elsewhere, redirect to the feed
            return redirect('feed')

    return redirect('feed')


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'post_detail.html', {'post': post})

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'profile.html', {'user': user})

def get_post_link(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post_url = request.build_absolute_uri(post.get_absolute_url())
    return JsonResponse({'url': post_url})

def track_share(request):
    return JsonResponse({'message': 'Profile share tracked successfully!'})

def share_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    share_url = request.build_absolute_uri(reverse('post_detail', args=[post.id]))
    return HttpResponse(f"Share this link: <a href='{share_url}'>{share_url}</a>")
