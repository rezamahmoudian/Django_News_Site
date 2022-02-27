from django.forms import ModelForm
from .models import User


class ProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        #گرفتن kwargs که در ویوو توسط تابع get_kwargs_model ارسال شد
        #حتما باید بالاتر از super باشد تا کی و ولیوی user قبل از ارسال ب super با متد پاپ پاک شوند
        user = kwargs.pop('user')

        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        if not user.is_superuser:
            self.fields['username'].widget.attrs['readonly'] = True
            self.fields['email'].widget.attrs['readonly'] = True
            self.fields['vip_user'].widget.attrs['readonly'] = True
            self.fields['is_author'].widget.attrs['readonly'] = True

    class Meta:
        model = User
        fields = ['username', 'first_name','last_name', 'email', 'vip_user', 'is_author']
