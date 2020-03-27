from django import template

from mytutor.models import *

register = template.Library()


@register.simple_tag(name="is_booked_by_student", takes_context=True)
def is_booked_by_student(context, id):
    request = context['request']
    if request.user.is_authenticated:
        if Booking.objects.filter(student_id=request.user.id, teacher_id=id):
            return True
        else:
            return False
    else:
        return False
