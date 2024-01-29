from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .filters import PostFilter, FeedbackFilter
from .forms import PostForm, UserForm, FeedbackForm
from .models import Post, Category, Feedback, User
from .tasks import send_user_email


# Create your views here.


class AuthorRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if not request.user.is_authenticated or obj.author != request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class PostListView(ListView):
    model = Post
    ordering = '-create_datetime'
    template_name = 'request_post_list.html'
    context_object_name = 'request_post_list'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filerset'] = self.filterset
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'request_post_detail.html'
    context_object_name = 'request_post_detail'


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'request_post_create.html'
    context_object_name = 'request_post_create'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)


class PostUpdateView(AuthorRequiredMixin, LoginRequiredMixin, UpdateView):  # AuthorRequiredMixin
    form_class = PostForm
    model = Post
    template_name = 'request_post_update.html'


class PostDeleteView(AuthorRequiredMixin, LoginRequiredMixin, DeleteView):  # AuthorRequiredMixin
    model = Post
    template_name = 'request_post_delete.html'
    success_url = '/'


class CategoryListView(ListView):
    model = Category
    ordering = 'id'
    template_name = 'category_list.html'
    context_object_name = 'category_list'
    paginate_by = 5


class CategoryDetailView(DetailView):
    model = Post
    ordering = '-create_datetime'
    template_name = 'category_detail.html'
    context_object_name = 'category_detail'


class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user_detail'


class UserUpdateView(LoginRequiredMixin, UpdateView):  # AuthorRequiredMixin
    form_class = UserForm
    model = User
    template_name = 'user_update.html'
    context_object_name = 'user_update'
    success_url = '/'  # ??


class FeedbackCreateView(LoginRequiredMixin, CreateView):
    form_class = FeedbackForm
    model = Feedback
    template_name = 'comment_create.html'
    context_object_name = 'comment_create'

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.post_id = self.kwargs['pk']
        comment.save()
        send_user_email.delay(comment.post.author.email)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('request_post_detail', kwargs={'pk': self.kwargs['pk']})


class FeedbackListView(ListView):
    model = Feedback
    ordering = 'id'
    template_name = 'post_comment_list.html'
    context_object_name = 'post_comment_list'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset().filter(post__author=self.request.user)
        self.filterset = FeedbackFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filerset'] = self.filterset
        return context


class FeedbackAcceptView(View):
    def get(self, request, pk):
        feedback = get_object_or_404(Feedback, id=pk)
        feedback.accept()
        send_user_email.delay(feedback.author.email)
        return redirect('post_feedback_list')


class FeedbackDeleteView(View):
    def get(self, request, feedback_id):
        feedback = get_object_or_404(Feedback, id=feedback_id)
        feedback.delete()
        return redirect('post_feedback_list')


