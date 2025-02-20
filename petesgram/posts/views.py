from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
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
    user_to_follow = get_object_or_404(User, username=username)
    profile = request.user.profile
    target_profile = user_to_follow.profile
    
    if profile.following.filter(id=user_to_follow.id).exists():
        profile.following.remove(user_to_follow)
        action = 'unfollowed'
    else:
        profile.following.add(user_to_follow)
        action = 'followed'
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': action,
            'followers_count': target_profile.followers.count(),
            'following': not profile.following.filter(id=user_to_follow.id).exists()
        })
    return redirect('feed')