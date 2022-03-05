from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True,verbose_name="ایمیل")
    is_author = models.BooleanField(default=False,verbose_name='وضعیت نویسندگی')
    vip_user = models.DateTimeField(default=timezone.now, verbose_name='کاربر وی آی پی تا')
    profile_img = models.ImageField(upload_to="images", default="images/avatar5.png", verbose_name='عکس پروفایل')
    def is_vip_user(self):
        if self.vip_user > timezone.now():
            return True
        else:
            return False
    is_vip_user.short_description = 'کاربر ویژه'
    is_vip_user.boolean = True

