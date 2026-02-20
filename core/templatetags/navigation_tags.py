from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def active_class(context, url_name):
    request = context.get("request")
    if request and request.resolver_match and request.resolver_match.view_name == url_name:
        return "text-cyan-400"
    return "text-slate-200 hover:text-cyan-300"
