from django.contrib import admin
from .models import Category, Post, Comment

# Register Category model
admin.site.register(Category)
# Register Post model
admin.site.register(Post)
# Register Comment model
admin.site.register(Comment)
