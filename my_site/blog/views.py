from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Article, Category, IP_Address
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from acount.models import User
from acount.mixins import AccessUpdateForm

# Create your views here.


def homeView(request, page_number=1):
    post_lists = Article.objects.published()
    paginator = Paginator(post_lists, 6)
    posts = paginator.get_page(page_number)
    categorys = Category.objects.filter(status=True)
    dic = {'posts': posts,
           'categorys': categorys}
    print("posts in home = " , posts)
    return render(request, 'blog/home.html', dic)


def aboutView(request):
    dic = {}
    return render(request, 'blog/about.html', dic)


def contactView(request):
    dic = {}
    return render(request, 'blog/contact.html', dic)


def postView(request, slug):
    post = get_object_or_404(Article, slug=slug, status='p')
    dic = {'post': post}
    ip_address = request.user.ip_address
    print(ip_address)
    if not ip_address in post.hits.all():
        post.hits.add(ip_address)

    return render(request, 'blog/post.html', dic)


# def categoryView(request, slug, page_number=1):
#     category = get_object_or_404(Category.objects.active(), slug=slug)
#     post_lists = category.posts.published()
#     paginator = Paginator(post_lists, 2)
#     posts = paginator.get_page(page_number)
#
#     # posts = get_object_or_404(Article.category, slug=slug, status=True)
#     dic = {
#         "category": category,
#         "posts": posts
#     }
#     return render(request, 'blog/category.html', dic)


class CategoryListView(ListView):
    paginate_by = 6
    template_name = "../templates/blog/category.html"

    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.filter(status=True), slug=slug)
        return category.posts.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context

class AuthorListView(ListView):
    paginate_by = 6
    template_name = "../templates/blog/author_list.html"

    def get_queryset(self):
        global author
        username = self.kwargs.get('username')
        author = get_object_or_404(User, username=username)
        return author.posts.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = author
        return context


class PreviewPostView(AccessUpdateForm, DetailView):
    def get_queryset(self):
        pk= self.kwargs.get('pk')
        return Article.objects.filter(pk = pk)
    template_name = 'blog/preview_post.html'