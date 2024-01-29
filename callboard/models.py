from django.db import models

from django.contrib.auth.models import User

from tinymce.models import HTMLField

from django.template.defaultfilters import slugify
import os


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    create_datetime = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')  # default=Category.id == 1)  #
                                                                        # through='RequestPostCategory'
    title = models.CharField(max_length=200)
    content = HTMLField()  # tinymce HTMLField

    def get_absolute_url(self):
        return f"/callboard/{self.id}"

    def __str__(self):
        return self.title


class Feedback(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='feedbacks')
    create_datetime = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=1000)
    accept_status = models.BooleanField(default=False)  # !!

    def accept(self):
        self.accept_status = True
        self.save()
