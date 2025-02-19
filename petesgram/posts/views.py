
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Like, Comment
from .forms import PostForm


def feed(request):
    posts = Post.objects.all()

    # If user is not authenticated, set liked_posts to an empty list
    if request.user.is_authenticated:
        liked_posts = Like.objects.filter(user=request.user).values_list('post_id', flat=True)
    else:
        liked_posts = []  # Prevents error for anonymous users

    context = {
        'posts': posts,
        'liked_posts': liked_posts,
    }
    return render(request, 'posts/feed.html', context)

def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('feed')
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()  # Unlike if already liked
    return redirect('feed')

@login_required
def comment_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        text = request.POST.get("comment")
        if text:
            Comment.objects.create(user=request.user, post=post, text=text)
    return redirect('feed')