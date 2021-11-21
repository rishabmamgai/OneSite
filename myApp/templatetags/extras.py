from django import template
import json


# Auxilary function
def sorter(item):
    """
        Used to sort dict alphabetically 

        Example:
            dict(sorted(dictionary.items(), key=sorter))
    """

    return item[0]


register = template.Library()


@register.filter(name='get_keys')
def get_keys(obj):
    marks_mid = json.loads(obj[0].mid_sem)

    mid = dict(sorted(marks_mid.items(), key=sorter))

    return mid.keys()


@register.filter(name='get_mid')
def get_mid(obj):
    mid = json.loads(obj[0].mid_sem)

    marks = []

    mid = dict(sorted(mid.items(), key=sorter))
    for key in mid.keys():
        marks.append(mid[key])

    return marks


@register.filter(name='get_end')
def get_end(obj):
    query_result = obj[0].end_sem

    if len(query_result) == 0:
        return ['-']*6

    else:
        end = json.loads(query_result)
        
        marks = []

        end = dict(sorted(end.items(), key=sorter))

        for key in end.keys():
            marks.append(end[key])

        return marks


@register.filter(name='get_practical')
def get_practical(obj):
    query_result = obj[0].practicals

    if len(query_result) == 0:
        return ['-']*6

    else:
        mid = json.loads(obj[0].mid_sem)
        practical = json.loads(query_result)
        
        marks = []

        mid = dict(sorted(mid.items(), key=sorter))
        for key in mid.keys():

            if key in practical.keys():
                marks.append(practical[key])
            
            else:
                marks.append('-')

        return marks
