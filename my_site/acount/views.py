from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from blog.models import Article
from .models import User
from .forms import ProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import CreateFieldsMixin, FormValidMixin, AccessUpdateForm, AccessAuthors,AccessAdmins
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
#برای شخصی سازی ارورهای لاگین
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage

from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.

app_name = 'acount'

@login_required
def home(request, ):
    return render(request, 'registration/home.html')

#یک ویوو برای نمایش لیست مقالات
#به آن میکسین هایی داده شده است که دسترسی ها به این ویوو را مدیریت میکنند
class ArticleListView(LoginRequiredMixin, AccessAuthors, ListView):
    template_name = 'registration/home.html'
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author=self.request.user)

#یک ویوو برای نوشتن مقاله ی جدید توسط نویسندگان
#به آن میکسین هایی داده شده است که دسترسی ها به این ویوو را مدیریت میکنند
class ArticleCreateView(LoginRequiredMixin, AccessAuthors, FormValidMixin, CreateFieldsMixin, CreateView):
    model = Article
    template_name = 'registration/create_article.html'
#ویوو ویرایش مقالات
class ArticleUpdateView(LoginRequiredMixin, AccessAuthors, AccessUpdateForm, FormValidMixin, CreateFieldsMixin, UpdateView):
    model = Article
    template_name = 'registration/create_article.html'

#ویوو پروفایل
class ProfileView(LoginRequiredMixin, UpdateView):
    #چون میخواهیم پروفایلمان متشکل از یک فرم باشد پس به آن یوز(که میخواهیم اطلاعات آن در فرم نمایش داده شوند و یا ویرایش شوند)
    #وهمینطور فرمی که در فرم ها ساختیم را میدهیم
    #و یک تمپلیت به آن میدهیم که فرم ما به آ« وصل شئد
    #به عبارت دیگر ابتدا یوزر را به فرم میفرستیم و س÷س فرم را به تمپلیت میفرستیم
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


#یک ویوو برای حذف مقالات
#به آن دو میکسین داده شده است که دسترسی ها به این ویوو را مدیریت میکنند
class ArticleDeleteView(LoginRequiredMixin, AccessUpdateForm, DeleteView):
    model = Article
    success_url = reverse_lazy("acount:home")
    template_name = 'registration/delete_article.html'

#شخصی سازی ارورهای صفحه ی لاگین
class MyAuthForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _(
            render_to_string('registration/login_error.html')
        ),
        'inactive': _("اکانت شما فعال نیست لطفا آنرا فعال کنید"),
    }

#سفارشی کردن لاگین ویوو جنگو
class Login(LoginView):
    authentication_form = MyAuthForm
    template_name = 'registration/login.html'
    #نمیدونم چرا این کار نمیکنه بخاطر همین با میکسین ها مشکل رو حل کردم
    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy ("acount:home")
        else:
            print("go to profile")
            return reverse_lazy ("acount:profile")


#ویوو صفحه ی ثبت نام
class Signup(CreateView):
    form_class = SignupForm
    template_name = 'registration/signup.html'
    #به ویوو یک فرم داده میشود
    #اگر فرم ارسالی ولید بود ایمیلی جهت تایید برای کاربر ارسال شود


    def send_activation_email(self, request, user):
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your account.'
        message = render_to_string('registration/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = user.email
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()


    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        self.send_activation_email(self.request, user)
        return render(self.request, 'registration/signup_email_confirm.html')



    # تابعی که قبل از چک شدن ولید بودن فرم فراخوانی میشود ما با اوور راید کردن این تابع
    # ابتدا چک میکنیم که آیا نام کاربری و ایمیل انتخاب شده قبلا ثبت نام کرده اند یا نه
    # اگر قبلا ثبت نام کرده بودند چک میکنیم که آیا اکانت آن شخص غیرفعال است؟ و اگر اکانت شخص فعال نبود
    #  برای او ایمیلی جهت فعالسازی اکانتش ارسال میکنیم و از ادامه ی فرایند ثبت نام جلوگیری میکنیم
    #  اما اگر آن شخص اکانت غیر فعال نداشت و یا اصلا اکانتی نداشت مراحل ثبت نام بصورت معمولی طی میشوند
    def post(self, request, *args, **kwargs):
        """ Handles existing inactive user registration attempt """
        form = self.form_class(self.request.POST)
        if User.objects.filter(email=request.POST['email']).exists():
            user = User.objects.get(email=request.POST['email'])
            if not user.is_active:
                self.send_activation_email(request, user)
                return render(self.request, 'registration/signup_email_confirm.html')
        # if no record found pass to form_valid
        return super().post(request, *args, **kwargs)


#فغالسازی اکانت درصورت کلیک روی لینک ایمیل شده
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'registration/signup_email_confirm_done.html')
    else:
        return HttpResponse('لینک فعالسازی منقضی شده است')



#ویوو پروفایل برای دسترسی ادمین ها به پروفایل نویسندگان
class UsersProfile(LoginRequiredMixin,AccessAdmins, UpdateView):
    #چون میخواهیم پروفایلمان متشکل از یک فرم باشد پس به آن یوز(که میخواهیم اطلاعات آن در فرم نمایش داده شوند و یا ویرایش شوند)
    #وهمینطور فرمی که در فرم ها ساختیم را میدهیم
    #و یک تمپلیت به آن میدهیم که فرم ما به آ« وصل شئد
    #به عبارت دیگر ابتدا یوزر را به فرم میفرستیم و س÷س فرم را به تمپلیت میفرستیم
    model = User #اینجا فقط مشخص میکنیم که مدل ما از نوع یوزر است و پایین تر مشخص میشود که کدام یوزر باید به فرم ارسال شود
    form_class = ProfileForm
    template_name = 'registration/profile_users.html'

    def get_success_url(self,*args, **kwargs):
        return reverse_lazy ('acount:users_profile', kwargs={'pk':self.kwargs.get('pk')})


    # بعد از ایجاد تغییر در اطلاعات یوزر اگر که ادمین یوزر را نویسنده کرد درخواست نویسندگی او فالس شود
    def form_valid(self, form):
        user = form.save(commit=False)
        if user.is_author:
            user.author_request = False
        user.save()
        return super(UsersProfile, self).form_valid(form)

    #فرستادن یوزر به فرم به عنوان آبجکت که باعث میشود فرم نمایش داده شده مربوط به همان یوزری باشد که لاگین کرده است
    def get_object(self, *args, **kwargs):
        #یوزری که آی دی آن در url آمده است به فرم ارسال میشود
        user = User.objects.get(id=self.kwargs.get('pk'))
        return user

    #آپدیت کردن kwargs برای ارسال به فرم و ایجاد ارتباط بین ویوو و فرم
    #فرستادن یوزر با اضافه کردن آن در دیکشنری kwargs که باعث میشود ما در فرم هم به یوزر دسترسی داشته باشیم و شرط سوپر یوزر بودن را ب کار ببریم
    def get_form_kwargs(self):
        kwargs = super(UsersProfile, self).get_form_kwargs()
        #اینجا یوزر لاگین کرده که همان ادمین است را به فرم ارسال میکنیم تا سطح دسترسی به فرم ها بر اساس دسترسی های ادمین باشد
        kwargs['user'] = self.request.user
        return kwargs

#یک ویوو برای حذف مقالات
#به آن دو میکسین داده شده است که دسترسی ها به این ویوو را مدیریت میکنند
class ArticleDeleteView(LoginRequiredMixin, AccessUpdateForm, DeleteView):
    model = Article
    success_url = reverse_lazy("acount:home")
    template_name = 'registration/delete_article.html'


# class RecuestAuthorView(UpdateView):
#     model = User
#     form_class = RecuestAuthorForm
#     template_name = 'registration/profile.html'
#     success_url = reverse_lazy("acount:profile")


# وقتی کاربر بر روی دکمه ی درخواست نویسندگی کلیک کند این تابع فراخوانی شده و درخئاست کاربر ارسال میشود
def author_request(request):
    user = request.user
    user.author_request = True
    user.save()
    # انتقال به صفحه ی پروفایل بعد از اتمام کار تابع
    return HttpResponseRedirect(reverse('acount:profile'))



#یک ویوو برای نمایش لیست مقالات
#به آن میکسین هایی داده شده است که دسترسی ها به این ویوو را مدیریت میکنند
class UserListView(LoginRequiredMixin, AccessAdmins, ListView):
    template_name = 'registration/user_list.html'
    def get_queryset(self):
        return User.objects.filter(is_superuser=False).order_by('-author_request')
