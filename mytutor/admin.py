from django import forms
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.admin import UserAdmin

from mytutor.models import *


class CourseTeacherAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CourseTeacherAdminForm, self).__init__(*args, **kwargs)
        self.fields['teacher'] = forms.ModelChoiceField(queryset=User.objects.filter(role="teacher"))

    def clean(self):
        super().clean()
        if CourseTeacher.objects.filter(teacher=self.cleaned_data['teacher'], course=self.cleaned_data['course']):
            raise forms.ValidationError("Teacher is already assigned to the course")


class CourseTeacherAdmin(admin.ModelAdmin):
    form = CourseTeacherAdminForm


# class UserCreateForm(UserCreationForm):
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)
#
#     class Meta:
#         model = User
#         fields = "__all__"
#
#     def save(self, commit=True):
#         # Save the provided password in hashed format
#         user = super(UserCreateForm, self).save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user
#
#
# class CustomUserAdmin(UserAdmin):
#     add_form = UserCreationForm
#     prepopulated_fields = {'username': ('first_name', 'last_name',)}


admin.site.register(User)
admin.site.register(Subject)
admin.site.register(Course)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(CourseTeacher, CourseTeacherAdmin)
