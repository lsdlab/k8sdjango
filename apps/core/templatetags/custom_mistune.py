# from django import template
# from django.template.defaultfilters import stringfilter
# from django.utils.safestring import mark_safe
# import mistune
# # from apps.core.custom_mistune_render import CustomMistuneRenderer


# register = template.Library()


# @register.filter(is_safe=True)
# @stringfilter
# def custom_mistune(value):
#     # renderer = CustomMistuneRenderer()
#     # mistune_markdown = mistune.Markdown(renderer=renderer)
#     # return mark_safe(mistune_markdown(value))
#     return mark_safe(mistune.markdown(value))
