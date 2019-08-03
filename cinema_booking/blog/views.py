from django.shortcuts import render
from .models import Category, Post
from django.views.generic import (ListView, DetailView)

# View to display results on searching for posts
class PostSearchView(ListView):
    model = Post
    template_name = 'blog/post_search.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # getting the search string from search request
        post_title = self.request.GET.get('post_title')
        # get posts that contain the search string
        queryset = Post.objects.filter(title__icontains=post_title)
        return queryset

# Home page view -> listing the posts posted so far
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'

# List the posts according to the categories
class PostCategoryListView(ListView):
    template_name = 'blog/home.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # getting slug of category from URL
        slug = self.kwargs.get('slug')
        # getting posts that are of same category
        queryset = Post.objects.filter(category__slug__iexact=slug)
        return queryset

# Display the post and its content
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
