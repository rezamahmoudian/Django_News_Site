from django.http.response import  Http404
from django.shortcuts import get_object_or_404
from blog.models import Article

class CreateFieldsMixin():
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            self.fields = ['author','title','slug','category','content','image','status']
        elif self.request.user.is_author:
            self.fields = ['title', 'slug', 'category', 'content', 'image']
        else:
            raise Http404("شما به این صفحه دسترسی ندارید.")
        return super().dispatch(request, *args, **kwargs)


class FormValidMixin():
    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.save()
        elif self.request.user.is_author:
            self.obj = form.save(commit=False)
            self.obj.author = self.request.user
            self.obj.status = 'd'
        return super().form_valid(form)


class AccessUpdateForm():
    def dispatch(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        if self.request.user.is_superuser or article.author == request.user and article.status == 'd' or article.author == request.user and article.status == 'b' :
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("شما به این صفحه دسترسی ندارید.")

