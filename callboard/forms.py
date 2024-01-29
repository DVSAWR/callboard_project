from django import forms

from django.urls import reverse

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from allauth.account.forms import SignupForm

from .models import Post, Category, Feedback, User

from tinymce.widgets import TinyMCE


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        widgets = {'content': TinyMCE(attrs={'cols': 10, 'rows': 30})}

        fields = ['title', 'category', 'content']


class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = ['content']  # !!


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

        def clean_email(self):
            email = self.cleaned_data.get('email')
            username = self.cleaned_data.get('username')
            if email and User.objects.filter(email=email).exclude(username=username).exists():
                raise forms.ValidationError('EMAIL NOT UNIQUE - USERNAME NOT UNIQUE')
            return email

        def get_absolute_url(self):
            return f"/user/{self.id}"
