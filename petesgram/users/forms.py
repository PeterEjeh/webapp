from django import forms
from django.contrib.auth.models import User
from .models import Profile, Upload
from posts.models import Post

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]

class UploadForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ["image", "video", "caption"]

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get("image")
        video = cleaned_data.get("video")

        if not image and not video:
            raise forms.ValidationError("Please upload either an image or a video.")
        return cleaned_data
    