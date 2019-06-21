from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.PostListView.as_view(), name='blog-home'),
    path('post/<slug:slug>/',
         views.PostDetailView.as_view(),
         name='post-detail'),
    path('category/<slug:slug>',
         views.PostCategoryListView.as_view(),
         name='post-category')
    #   path('blog/<int:pk>/', views.BlogDetailView.as_view() , name='blog-detail')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
