from django import template
from ..models import Category

register = template.Library()

@register.simple_tag
def title():
    return 'سایت رضا'


@register.inclusion_tag("../templates/blog/partials/navbar.html")
def navbar_tmp_tag():
    return {
        "categorys": Category.objects.filter(status=True)
    }

