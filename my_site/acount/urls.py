from django.contrib.auth import views
from django.urls import path
from .views import (ArticleListView,ArticleCreateView, ArticleUpdateView,
                    ArticleDeleteView, ProfileView, Login, UsersProfile,
                    author_request, UserListView, SearchView)

app_name = 'acount'

urlpatterns = [
    path('', ArticleListView.as_view() , name='home'),
    path('create_article/', ArticleCreateView.as_view() , name='create_atticle'),
    path('update_article/<int:pk>', ArticleUpdateView.as_view() , name='update_atticle'),
    path('profile/', ProfileView.as_view() , name='profile'),
    path('profile/<int:pk>', UsersProfile.as_view() , name='users_profile'),
    path('delete_article/<int:pk>', ArticleDeleteView.as_view() , name='delete_atticle'),
    path('profile/author_request', author_request, name='author_request' ),
    path('user_list', UserListView.as_view() , name='user_list'),
    path('search/',SearchView.as_view(), name='search'),
    path('search/<int:page>', SearchView.as_view(), name='search'),
]