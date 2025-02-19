from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# User Profile Model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    followers = models.ManyToManyField(User, related_name='following', blank=True)

    def toggle_follow(self, user):
        """Handle follow/unfollow toggle for the given user."""
        if user in self.followers.all():
            self.followers.remove(user)
            return False  # Not following anymore
        else:
            self.followers.add(user)
            return True  # Now following


    def __str__(self):
        return self.user.username



    # Signal to automatically create a profile for new users
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def followers_count(self):
        return self.followers.count()


# Post Model (For Images and Videos)
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')  # Fix added here
    image = models.ImageField(upload_to='posts/images/', blank=True, null=True)
    video = models.FileField(upload_to='posts/videos/', blank=True, null=True)
    caption = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)

    def __str__(self):
        return f'Post by {self.user.username} - {self.created_at.strftime("%Y-%m-%d")}'

    def likes_count(self):
        return self.likes.count()


# Comment Model
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')  # Fix added here
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.id}'


# Follow Relationship (Alternative method if not using ManyToManyField in Profile)
class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following_user', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers_user', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
