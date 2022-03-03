from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from blog.models import Article
from .models import User
from .forms import ProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import CreateFieldsMixin, FormValidMixin, AccessUpdateForm, AccessAuthors
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
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


class ArticleCreateView(LoginRequiredMixin, AccessAuthors, FormValidMixin, CreateFieldsMixin, CreateView):
    model = Article
    template_name = 'registration/create_article.html'

class ArticleUpdateView(LoginRequiredMixin, AccessAuthors, AccessUpdateForm, FormValidMixin, CreateFieldsMixin, UpdateView):
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


#سفارشی کردن لاگین ویوو جنگو
class Login(LoginView):
    template_name = 'registration/login.html'
    #نمیدونم چرا این کار نمیکنه بخاطر همین با میکسین ها مشکل رو حل کردم
    def get_success_url(self):
        if self.request.user.is_superuser:
            print("go to home")
            return reverse_lazy ("acount:home")
        else:
            print("go to profile")
            return reverse_lazy ("acount:profile")


class Signup(CreateView):
    form_class = SignupForm
    template_name = 'registration/signup.html'
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your account.'
        message = render_to_string('registration/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return HttpResponse("ایمیلی برای شما ارسال شد.لطفا برای تکمیل فرایند ثبت نام ایمیل خود را تایید کنید")



def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse("از شما برای تایید یمیل خود متشکریم.برای ورود به حساب کاریبری خود<'a href='registration/login'>کلیک کنید</a> ")
    else:
        return HttpResponse('لینک فعالسازی منقضی شده است')




# from django.contrib.auth import get_user_model
# from django.contrib.auth.tokens import default_token_generator
# from django.contrib.sites.shortcuts import get_current_site
# from django.core.mail import EmailMessage
# from django.http import HttpResponse
# from django.shortcuts import render
# from django.template.loader import render_to_string
# from django.utils.encoding import force_bytes
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
#
# UserModel = get_user_model()
# from .forms import SignupForm
# from .tokens import account_activation_token
#
#
# def signup(request):
#     if request.method == 'GET':
#         return render(request, 'accounts/signup.html')
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         # print(form.errors.as_data())
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()
#             current_site = get_current_site(request)
#             mail_subject = 'Activate your account.'
#             message = render_to_string('accounts/acc_active_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': default_token_generator.make_token(user),
#             })
#             to_email = form.cleaned_data.get('email')
#             email = EmailMessage(
#                 mail_subject, message, to=[to_email]
#             )
#             email.send()
#             return HttpResponse('Please confirm your email address to complete the registration')
#     else:
#         form = SignUpForm()
#     return render(request, 'accounts/signup.html', {'form': form})
#
#
# def activate(request, uidb64, token):
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = UserModel._default_manager.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     if user is not None and default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
#         return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
#     else:
#         return HttpResponse('Activation link is invalid!')