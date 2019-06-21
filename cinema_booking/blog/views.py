from django.shortcuts import render
from .models import Category, Post, Comment
from django.views.generic import (ListView, DetailView)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'


class PostCategoryListView(ListView):
    template_name = 'blog/home.html'
    context_object_name = 'posts'

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        queryset = Post.objects.filter(category__slug__iexact=slug)
        return queryset


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_list'] = Comment.objects.filter(
            post=context['object'].id)
        return context
