from django.contrib.auth import authenticate
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.template.loader import render_to_string
from importlib._common import _

from django.forms import ModelForm
from .models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm


class ProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        # گرفتن kwargs که در ویوو پروفایل توسط تابع get_kwargs_model ارسال شد
        # حتما باید بالاتر از super باشد تا کی و ولیوی user قبل از ارسال ب super با متد پاپ پاک شوند
        user = kwargs.pop('user')

        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        # غیرفعال کردن بعضی از فیلدهای پروفایل درصورت سوپر یوزر نبودن کاربر
        if not user.is_superuser:
            self.fields['username'].widget.attrs['readonly'] = True
            self.fields['email'].widget.attrs['readonly'] = True
            self.fields['vip_user'].widget.attrs['readonly'] = True
            self.fields['is_author'].disabled = True

    # نوشتن فیلدهایی که میخاهیم در فرممان ب آنها دسترسی داشته باشیم و از آنها استفاده کنیم
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'vip_user', 'is_author', 'profile_img']


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ResendEmailConfirmForm(ModelForm):
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ('email',)

    error_messages = {
        'invalid_email':
            render_to_string('registration/resend_email_confirm_errors.html')
        ,
        'inactive': render_to_string('registration/resend_email_confirm_errors.html'),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')

        if email is not None:
            self.user_cache = authenticate(self.request, email=email)
            if self.user_cache is None:
                raise self.get_invalid_email_error()

        return self.cleaned_data


    def get_user(self):
        return self.user_cache

    def get_invalid_email_error(self):
        return ValidationError(
            self.error_messages['invalid_email'],
            code='invalid_email',
            # params={'username': self.username_field.verbose_name},
        )
