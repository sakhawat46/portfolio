from django import template

register = template.Library()


@register.simple_tag
def page_title(meta_title, fallback):
    return meta_title or fallback
