from django import template

from mytutor.models import *

register = template.Library()


@register.simple_tag(name="is_enrolled_by_teacher", takes_context=True)
def is_enrolled_by_teacher(context, id):
    request = context['request']
    my_courses = request.user.my_courses.values_list("course_id", flat=True)
    if id in my_courses:
        return True
    else:
        return False
