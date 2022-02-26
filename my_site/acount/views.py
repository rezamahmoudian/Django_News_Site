from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from blog.models import Article
from .models import User
from .forms import ProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import CreateFieldsMixin, FormValidMixin, AccessUpdateForm
from django.urls import reverse_lazy
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

class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'registration/profile.html'
    success_url = reverse_lazy ("acount:profile")

    #فرستادن یوزر به فرم به عنوان آبجکت که باعث میشود فرم نمایش داده شده مربوط به همان یوزری باشد که لاگین کرده است
    def get_object(self):
        return self.request.user

    #آپدیت کردن kwargs برای ارسال به فرم و ایجاد ارتباط بین ویوو و فرم
    #فرستادن یوزر با اضافه کردن آن در دیکشنری kwargs که باعث میشود ما در فرم هم به یوزر دسترسی داشته باشیم و شرط سوپر یوزر بودن را ب کار ببریم
    def get_form_kwargs(self):
        kwargs = super(ProfileView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class ArticleDeleteView(LoginRequiredMixin, AccessUpdateForm, DeleteView):
    model = Article
    success_url = reverse_lazy("acount:home")
    template_name = 'registration/delete_article.html'



