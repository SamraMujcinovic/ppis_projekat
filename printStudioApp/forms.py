from django.forms import ModelForm, CharField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.validators import validate_email

from .models import CustomUser, Order, ContactUsForm


class OrderForm(forms.Form):
    PRINT_TYPE=[('1','One side'),('2','Two side')]
    BIND_TYPE=[('1','Claims'),('2','Soft'),('3','Spiral')]
    COLOR = [('4','Color'), ('2','Black-White')]

    orderCode = forms.CharField()
    title = forms.FileField()
    print_type = forms.ChoiceField(choices=PRINT_TYPE, widget=forms.RadioSelect)
    bind_type = forms.ChoiceField(choices=BIND_TYPE, widget=forms.RadioSelect)
    number_of_copies = forms.IntegerField()
    color = forms.ChoiceField(choices=COLOR, widget=forms.RadioSelect)

    fields = ['orderCode','title','print_type','bind_type','number_of_copies','color']



class CreateUserForm(UserCreationForm):
    phoneNumber = CharField()

    class Meta:
        model = User
        fields = ['email','password1','password2','first_name','last_name','username','phoneNumber']

class ContactForm(forms.Form):

    name = forms.CharField(initial='Your name')
    email = forms.EmailField(initial='Your email')
    message = forms.CharField()

    fields = ['name','email','message']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email( email )
            return email
        except ValidationError:
            return ("Enter valid email!")

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name == 'Your name':
            raise forms.ValidationError("Enter your name!")
        return name

    
