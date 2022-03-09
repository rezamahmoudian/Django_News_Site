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


@register.inclusion_tag("../templates/blog/partials/popular_article.html")
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
        "popular_articles": Article.objects.published().annotate(
            count=Count('views', filter=Q(articleviews__created__gt=last_month))
            ).order_by('-count', '-publish')[:5]
    }

