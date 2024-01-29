from django.contrib import admin

from .models import Post, Category, Feedback


class RequestPostAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Header', {'fields': ['title', 'category', 'author']}),
        ('Content', {'fields': ['content']}),
    ]


# Register your models here.

admin.site.register(Post, RequestPostAdmin)
admin.site.register(Category)
admin.site.register(Feedback)
