from django.urls import path

from .views import (PostListView, PostDetailView, PostCreateView, PostUpdateView,
                    PostDeleteView, UserDetailView, UserUpdateView, CategoryListView, FeedbackCreateView,
                    FeedbackDeleteView, FeedbackListView, FeedbackAcceptView)

urlpatterns = [
    path('', PostListView.as_view(), name='request_post_list'),
    path('<int:pk>', PostDetailView.as_view(), name='request_post_detail'),
    path('create/', PostCreateView.as_view(), name='request_post_create'),
    path('<int:pk>/update', PostUpdateView.as_view(), name='request_post_update'),
    path('<int:pk>/delete', PostDeleteView.as_view(), name='request_post_delete'),
    path('user/<int:pk>', UserDetailView.as_view(), name='user_detail'),
    path('user/<int:pk>/update', UserUpdateView.as_view(), name='user_update'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('callboard/<int:pk>/feedback', FeedbackCreateView.as_view(), name='feedback_create'),
    path('feedback/<int:feedback_id>', FeedbackDeleteView.as_view(), name='feedback_delete'),
    path('feedback/<int:pk>/accept', FeedbackAcceptView.as_view(), name='accept_feedback'),
    path('feedback/', FeedbackListView.as_view(), name='post_feedback_list')
]


