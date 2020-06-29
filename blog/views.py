from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import CommentForm
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import FormMixin
from .models import Post, Comment
from django.http import HttpResponseNotFound


class PostListView(ListView):
    model = Post
    template_name = 'blog/posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3


class CategoryPostListView(ListView):
    template_name = 'blog/posts.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        category = get_list_or_404(
            Post, category=self.kwargs.get('category'))
        return Post.objects.filter(
            category=self.kwargs['category']).order_by('-date_posted')


class DatePostListView(ListView):
    template_name = 'blog/posts.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        date = get_list_or_404(
            Post, date_posted__year=self.kwargs.get('year'), date_posted__month=self.kwargs.get('month'))
        return Post.objects.filter(date_posted__year=self.kwargs['year'],
                                   date_posted__month=self.kwargs['month']).order_by('-date_posted')


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/posts.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(FormMixin, DetailView):
    model = Post
    form_class = CommentForm

    def get_success_url(self):
        return(reverse('post-detail', kwargs={'pk': self.object.pk}) + '#comments-list')

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['form'] = CommentForm
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)

        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        if self.request.method == 'POST':
            parent_comment_id = self.request.POST.get("parent_id")
            form.instance.author = self.request.user
            form.instance.post = self.object

            if parent_comment_id:
                parent_comment_obj = get_object_or_404(
                    Comment, id=parent_comment_id)
                form.instance.parent = parent_comment_obj

        form.save()
        return super(PostDetailView, self).form_valid(form)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'category', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post

    def get_success_url(self):
        return reverse('blog-posts')

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        comment = self.get_object()
        post = comment.post
        return(reverse('post-detail', kwargs={'pk': post.pk}) + '#comments-list')

    def get_object(self):
        pk1 = self.kwargs['pk1']
        pk2 = self.kwargs['pk2']
        post = get_object_or_404(Post, pk=pk1)
        comment = get_object_or_404(Comment, pk=pk2)
        return comment

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author or self.request.user == comment.post.author:
            return True
        return False
