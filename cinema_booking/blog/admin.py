from django.contrib import admin
from .models import Category, Post

# Register Category model
admin.site.register(Category)
# Register Post model
admin.site.register(Post)