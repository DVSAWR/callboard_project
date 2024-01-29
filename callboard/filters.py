from django import forms

from .models import Post, Category, Feedback

from django_filters import FilterSet, DateFilter


class PostFilter(FilterSet):
    date = DateFilter(field_name='create_datetime',
                      widget=forms.DateInput(attrs={'type': 'date'}),
                      lookup_expr='date__gte',
                      label='Date is equal or greater then'
                      )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'author__username': ['icontains'],
            'category__name': ['icontains']
        }


class FeedbackFilter(FilterSet):

    class Meta:
        model = Feedback
        fields = {
            'author__username': ['icontains'],  #  только текущий пользователь
            'post__category': ['in'],
            'post__title': ['icontains'],
        }
