from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms

from mytutor.models import *


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    role = forms.CharField(max_length=12, help_text='Role is required')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'role']
        error_messages = {
            'first_name': {
                'required': 'First name is required',
                'max_length': 'First name is too long'
            },
            'last_name': {
                'required': 'Last name is required',
                'max_length': 'Last name is too long'
            },
            'username': {
                'required': 'Username is required',
                'max_length': 'Username is too long'
            },
            'email': {
                'required': 'Email is required',
                'email': 'Must be a valid email'
            },
            'role': {
                'required': 'Role is required'
            }
        }


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter Email'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Enter Password'})

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user = authenticate(email=email, password=password)

            if self.user is None:
                raise forms.ValidationError("User Does Not Exist.")
            if not self.user.check_password(password):
                raise forms.ValidationError("Password Does not Match.")
            if not self.user.is_active:
                raise forms.ValidationError("User is not Active.")

        return super(UserLoginForm, self).clean(*args, **kwargs)

    def get_user(self):
        return self.user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("education", "image", "description")
