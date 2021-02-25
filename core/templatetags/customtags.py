from django import template
register = template.Library()

@register.filter
def get(dictionary, key):
    if dictionary.get(key) and len(dictionary.get(key)) == 1:
        return dictionary.get(key, "")[0]
    elif dictionary.get(key, ""):
        return dictionary.get(key, "")
    else:
        return None

@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()
