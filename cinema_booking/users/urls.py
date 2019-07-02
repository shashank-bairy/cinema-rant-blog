from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'users'
urlpatterns = [
    path('<slug:slug>/',
         views.UserProfileDetailView.as_view(),
         name='user-profile-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)