from django.forms import ModelForm, CharField, fields
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.validators import validate_email
from django.forms.forms import Form

from .models import CustomUser, Order, ContactUsForm
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError



class OrderForm(forms.Form):
    PRINT_TYPE=[('1','One side'),('2','Two side')]
    BIND_TYPE=[('1','Claims'),('2','Soft'),('3','Spiral')]
    COLOR = [('1','Color'), ('2','Black-White')]

    orderCode = forms.CharField()
    title = forms.FileField()
    print_type = forms.ChoiceField(choices=PRINT_TYPE, widget=forms.RadioSelect)
    bind_type = forms.ChoiceField(choices=BIND_TYPE, widget=forms.RadioSelect)
    number_of_copies = forms.IntegerField()
    color = forms.ChoiceField(choices=COLOR, widget=forms.RadioSelect)

    fields = ['orderCode','title','print_type','bind_type','number_of_copies','color']

class ViewOrderForm(ModelForm):

    PRINT_TYPE=[('1','One side'),('2','Two side')]
    BIND_TYPE=[('1','Claims'),('2','Soft'),('3','Spiral')]
    COLOR = [('1','Color'), ('2','Black-White')]

    orderCode = forms.CharField(disabled=True)
    title = forms.FileField()
    print_type = forms.ChoiceField(choices=PRINT_TYPE, widget=forms.RadioSelect, disabled=True)
    bind_type = forms.ChoiceField(choices=BIND_TYPE, widget=forms.RadioSelect, disabled=True)
    number_of_copies = forms.IntegerField(disabled=True)
    color = forms.ChoiceField(choices=COLOR, widget=forms.RadioSelect, disabled=True)
    created_at = forms.DateTimeField(disabled=True)
    

    class Meta:
        model = Order
        fields = '__all__'
        
    
    def __init__(self, *args, **kwargs):
        super(ViewOrderForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['userID'].disabled=True



class CreateUserForm(UserCreationForm):
    phoneNumber = CharField()

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']

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

class ViewContactForm(ModelForm):

    name = forms.CharField(disabled = True)
    email = forms.EmailField(disabled=True)
    message = forms.CharField(disabled=True)

    class Meta:
        model = ContactUsForm
        fields = ['name', 'email','message']


class CustomUserForm(forms.Form):
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    phoneNumber = forms.CharField()
    
    fields = ['username','first_name','last_name','email','phoneNumber']

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['readonly'] = True

class CustomUserFormForAdmin(forms.Form):
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    phoneNumber = forms.CharField()
    
    fields = ['username','first_name','last_name','email','phoneNumber']

    def __init__(self, *args, **kwargs):
        super(CustomUserFormForAdmin, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['first_name'].widget.attrs['readonly'] = True
        self.fields['last_name'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['phoneNumber'].widget.attrs['readonly'] = True


class ChangePassword(PasswordChangeForm):
    old_password = forms.CharField(
        label=("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'off', 'autofocus': False}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)