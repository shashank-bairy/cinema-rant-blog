from django.shortcuts import render
from .models import Category, Post
from django.views.generic import (ListView, DetailView)


class PostSearchView(ListView):
    model = Post
    template_name = 'blog/post_search.html'
    context_object_name = 'posts'

    def get_queryset(self):
        post_title = self.request.GET.get('post_title')
        queryset = Post.objects.filter(title__icontains=post_title)
        return queryset


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
