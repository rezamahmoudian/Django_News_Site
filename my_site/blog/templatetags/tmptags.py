from django import template
from ..models import Article, Category , ArticleViews
from datetime import datetime, timedelta
from django.db.models import Count, Q

register = template.Library()

@register.simple_tag
def title():
    return 'سایت رضا'


@register.inclusion_tag("../templates/blog/partials/navbar.html")
def navbar_tmp_tag():
    return {
        "categorys": Category.objects.filter(status=True)
    }

#  برای نوشتن تمپلیت تگ باید آدرس تمپلیت خود را در اینکلوژن تگ زیر بنویسیم
#  و سپس تابعی تعریف میکنیم

@register.inclusion_tag("../templates/blog/partials/boxes.html")
def popular_articles(): # گرفتن مقالات پربازدید و ارسال آن به تمپلیت
    # بدست آوردن تاریخ یک ماه قبل
    last_month = datetime.today() - timedelta(days=30)

    """
    ایجاد کوِئری و بدست آوردن تعداد ویوهای یک آرتیکل با این فیلتر که آن ویوو ها مربوط به یک ماه قبل باشند
    (برای بدست آوردن ویووهای یک ماه قبل ابتدا یک مدل ساختیم
    که ویووهای هر مقاله را به عنوان کلید خارجی میگیرد و ب همراه تاریخ ویوو در دیتابیس ذخیره میکند
    مدل Articleviews و اینجا با کوئری زدن به این مدل و گرفتن فیلد create که زمان ویوو ها در آن إخیره شده اند
    ویوو هایی که طی یک ماه اخیر زده شده اند شمارش میشوند و مقاله ها متناسب با آن تعداد مرتب میشوند
    """
    return {
        "articles": Article.objects.published().annotate(
            count=Count('views', filter=Q(articleviews__created__gt=last_month))
            ).order_by('-count', '-publish')[:5],
        "title": "مقالات پربازدید ماه"
    }


@register.inclusion_tag("../templates/blog/partials/boxes.html")
def favorite_articles(): # گرفتن مقالات با امتیاز بالا و ارسال آن به تمپلیت
    last_month = datetime.today() - timedelta(days=30)
    return {
        "articles":  Article.objects.filter(ratings__isnull=False).annotate(count=Count('comments',
                     filter=Q(comments__posted__gt=last_month) and Q(comments__content_type_id=6)))
                                                      .order_by('-ratings__average', '-count', '-publish')[:5],
        "title":"مقالات محبوب"
    }


@register.inclusion_tag("../templates/blog/partials/boxes.html")
def hot_articles(): # گرفتن مقالات با امتیاز بالا و ارسال آن به تمپلیت
    last_month = datetime.today() - timedelta(days=30)
    return {
        "articles": Article.objects.published().annotate(count=Count('comments',
                    filter= Q(comments__posted__gt=last_month) and Q(comments__content_type_id=6)))
                    .order_by('-count', '-ratings__average', '-publish')[:5],
        "title":"مقالات داغ ماه"
    }



