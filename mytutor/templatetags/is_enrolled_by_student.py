from django import template

from mytutor.models import *

register = template.Library()


@register.simple_tag(name="is_enrolled_by_student", takes_context=True)
def is_enrolled_by_student(context, id):
    request = context['request']
    if request.user.is_authenticated:
        if EnrolledCourse.objects.filter(user_id=request.user.id, course_id=id):
            return True
        else:
            return False
    else:
        return False
