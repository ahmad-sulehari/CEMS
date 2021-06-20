from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from .models import MyUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = MyUser
        fields = [
            'f_name', 'l_name', 'date_of_birth', 'gender', 'email', 'password', 'degree', 'section', 'session',
            'student_id_number', 'student_id', 'phone_number'
        ]


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = MyUser
        fields = [
            'f_name', 'l_name', 'date_of_birth', 'gender', 'email', 'password', 'degree', 'section', 'session',
            'student_id_number', 'student_id', 'phone_number'
        ]


class CustomRequiredItemForm(ModelForm):
    pass
