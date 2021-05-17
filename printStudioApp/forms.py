from django.forms import ModelForm, CharField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import CustomUser, Order


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class CreateUserForm(UserCreationForm):
    phoneNumber = CharField()

    class Meta:
        model = User
        fields = ['email','password1','password2','first_name','last_name','username','phoneNumber']