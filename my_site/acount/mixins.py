from django.http.response import  Http404
from django.shortcuts import get_object_or_404, redirect
from blog.models import Article

#دسترسی به فرم ساخت مقاله برای ابرکاربر ها و نویسنده های معمولی
class CreateFieldsMixin():
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            self.fields = ['author','title','slug','category','content','image', 'special', 'status']
        elif self.request.user.is_author:
            #نویسنده ی معمولی به فیلد های انتخاب نویسنده برای مقاله دسترسی ندارد
            self.fields = ['title', 'slug', 'category', 'content', 'image', 'special', 'status']
            #برای وضعیت مقاله عدم دسترسی به انتشار و یا برگشت دادن مقاله در  در تمپلیت ایجاد مقاله انجام شده است
        else:
            raise Http404("شما به این صفحه دسترسی ندارید.")
        return super().dispatch(request, *args, **kwargs)

#میکسین ولید بودن فرم برای ذخیره ی مقاله ی جدید
class FormValidMixin():
    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.save()
            #اگر نویسنده ی مقاله نویسنده ی معمولی باشد فقط اجازه دارد که مقاله را در حالت پیشنویس قرار دهد یا آنرا برای ادمین ها ارسال کند و توانایی انتشار ندارد
        elif self.request.user.is_author:
            self.obj = form.save(commit=False)
            self.obj.author = self.request.user
            if not self.obj.status == 'i':
                self.obj.status = 'd'
        return super().form_valid(form)


#دسترسی به فرم ویرایش مقالات
class AccessUpdateForm():
    def dispatch(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        #کاربر یا باید ابر کاربر باشد یا اینکه نویسنده ی همان مقاله باشد تا بتواند آنرا ویرایش کند
        #البته یک نویسنده ب شرطی میتواند به صفحه ی ویرایش مقاله اش وارد شود که آن مقاله پیشنویس باشد یا اینکه ادمین آنرا برای ویرایش برگشت داده باشد
        if self.request.user.is_superuser or article.author == request.user and article.status == 'd' or article.author == request.user and article.status == 'b' :
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("شما به این صفحه دسترسی ندارید.")

#دسترسی به صفحات مربوط به نوشتن یا ویرایش مقاله

class AccessAuthors():
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            # کاربر یا باید نویسنده باشد یا ابر ماربر تا به این صفحات دسترسی پیدا کند
            if self.request.user.is_superuser or self.request.user.is_author :
                return super().dispatch(request, *args, **kwargs)
            else:
                #د غیر این صورت به پروفایل فرستاده میشود
                return redirect("acount:profile")
        else:
            #اگر لاگین نکرده باشد با زدن url مربوط به این صفحات به صفحه ی لاگین فرستاده میشود
            return redirect("login")


class AccessAdmins():
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            # کاربر باید ادمین(سوپریوزر)باشد تا به این صفحات دسترسی پیدا کند
            if self.request.user.is_superuser :
                return super().dispatch(request, *args, **kwargs)
            else:
                #د غیر این صورت به پروفایل فرستاده میشود
                return redirect("acount:profile")
        else:
            #اگر لاگین نکرده باشد با زدن url مربوط به این صفحات به صفحه ی لاگین فرستاده میشود
            return redirect("login")

class LoginAccess():
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            # اگر کاربر لاگین کرده باشد و نویسنده یا ادمین باشد به صفحه مقالات ریدایرکت میشود
            if self.request.user.is_superuser or self.request.user.is_author :
                return redirect("acount:home")
            else:
                # اگر لاگین کرده باشد و نویسنده یا ادمین هم نباشد به صفحه ی پروفایلش میرود
                return redirect("acount:profile")
        else:
            #در غیر این صورت به صفحه ی لاگین میرود
            return super().dispatch(request, *args, **kwargs)

