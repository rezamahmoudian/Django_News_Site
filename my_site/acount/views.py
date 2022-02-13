from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from blog.models import Article
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import CreateFieldsMixin, FormValidMixin, AccessUpdateForm
# Create your views here.

app_name = 'acount'

@login_required
def home(request, ):
    return render(request, 'registration/home.html')

class ArticleListView(LoginRequiredMixin, ListView):
    template_name = 'registration/home.html'
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author=self.request.user)


class ArticleCreateView(LoginRequiredMixin, FormValidMixin, CreateFieldsMixin, CreateView):
    model = Article
    template_name = 'registration/create_article.html'

class ArticleUpdateView(LoginRequiredMixin, AccessUpdateForm, FormValidMixin, CreateFieldsMixin, UpdateView):
    model = Article
    template_name = 'registration/create_article.html'



