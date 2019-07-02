from django.shortcuts import render
from .models import UserProfile
from blog.models import Post
from django.views.generic import DetailView

class UserProfileDetailView(DetailView):
    model = UserProfile
    context_object_name = 'user_profile'
    template_name = 'users/user_profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(author__id=context['object'].user.id)[:5]
        return context
