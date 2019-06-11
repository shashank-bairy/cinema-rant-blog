from django.contrib import admin
from .models import Post, Comment

# Register Post model
admin.site.register(Post)
# Register Comment model
admin.site.register(Comment)
