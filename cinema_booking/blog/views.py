from django.shortcuts import render
from .models import Category, Post, Comment
from django.views.generic import (ListView, DetailView)
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, get_list_or_404

# def search_posts(request):
#     if request.method == 'GET':
#         post_title = request.GET.get('post_title')
#         try:
#             status = Post.objects.filter(title__icontains=post_title)
#         except Post.DoesNotExist:
#             status = None
#         return render(request, 'blog/post_search.html', {"posts": status })
#     else:
#         return render(request, 'blog/post_search.html',{})


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_list'] = Comment.objects.filter(
            post=context['object'].id)
        return context
