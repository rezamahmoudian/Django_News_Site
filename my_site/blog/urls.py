from django.urls import path, include
from .views import ArticleListView, aboutView, contactView, postView, CategoryListView, AuthorListView, PreviewPostView

app_name = 'blog'
urlpatterns = [
    path('', ArticleListView.as_view(), name='home'),
    path('<int:page>', ArticleListView.as_view(), name='home'),
    path('about', aboutView, name='about'),
    path('contact', contactView, name='contact'),
    path('post/<slug:slug>', postView, name='post'),
    path('category/<slug:slug>',CategoryListView.as_view(), name='category'),
    path('category/<slug:slug>/<int:page>', CategoryListView.as_view(), name='category'),
    path('author/<slug:username>',AuthorListView.as_view(), name='author'),
    path('author/<slug:username>/<int:page>', AuthorListView.as_view(), name='author'),
    path('preview-post/<int:pk>', PreviewPostView.as_view() , name='preview-post'),
]