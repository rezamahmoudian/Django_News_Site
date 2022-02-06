from django.contrib import admin
from .models import Article, Category

# my changes in admin html page
admin.site.site_header = "صفحه ی مدیریت"
# Register your models here.

def make_publish(modeladmin, request, queryset):
    row_update = queryset.update(status='p')
    if row_update==1:
        message = 'منتشر شد'
    else:
        message = 'منتشر شدند'
    modeladmin.message_user(request, "{} مقاله {}".format(row_update,message))
make_publish.short_description = 'انتشار مقالات انتخاب شده'

def make_draft(modeladmin, request, queryset):
    row_update = queryset.update(status='d')
    if row_update == 1:
        message = 'پیش نویس شد'
    else:
        message = 'پیش نویس شدند'
    modeladmin.message_user(request, "{} مقاله {}".format(row_update, message))
make_draft.short_description = 'پیش نویس کردن مقالات انتخاب شده'


class AdminArticle(admin.ModelAdmin):
    list_display = ('title', 'image_post_adminpage', 'author', 'slug', 'jpublish', 'status', 'category_to_str')
    list_filter = ('publish', 'status')
    ordering = ('-status', '-publish')
    search_fields = ('title', 'slug', 'content')
    prepopulated_fields = {'slug': ('title', )}
    actions = [make_publish,make_draft]




class AdminCategory(admin.ModelAdmin):
    list_display = ('position', 'title', 'slug', 'parent', 'status')
    list_filter = (['status'])
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title', )}



admin.site.register(Article, AdminArticle)
admin.site.register(Category, AdminCategory)
