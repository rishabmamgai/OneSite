from django import template


register = template.Library()


@register.filter(name='sort')
def sort(branch_list):
    return sorted(branch_list)
