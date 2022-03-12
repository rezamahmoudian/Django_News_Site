from django.contrib.auth import views
from django.urls import path
from .views import ArticleListView,ArticleCreateView, ArticleUpdateView, ArticleDeleteView, ProfileView, Login

app_name = 'acount'

urlpatterns = [
    path('', ArticleListView.as_view() , name='home'),
    path('create_article/', ArticleCreateView.as_view() , name='create_atticle'),
    path('update_article/<int:pk>', ArticleUpdateView.as_view() , name='update_atticle'),
    path('profile/', ProfileView.as_view() , name='profile'),
    path('delete_article/<int:pk>', ArticleDeleteView.as_view() , name='delete_atticle'),
]

