from django.forms import ModelForm, CharField, fields, widgets
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
    print_type = forms.ChoiceField(choices=PRINT_TYPE, widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    bind_type = forms.ChoiceField(choices=BIND_TYPE, widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    number_of_copies = forms.IntegerField()
    color = forms.ChoiceField(choices=COLOR, widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    message = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder':'Leave a message if you have additional requirements...'}))


    fields = ['orderCode','title','print_type','bind_type','number_of_copies','color','message']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['orderCode'].widget.attrs.update({'class': 'form-control','placeholder': 'Order code'})
        self.fields['number_of_copies'].widget.attrs.update({'placeholder': 'Number of copies'})
        self.fields['print_type'].widget.attrs.update({'class': "custom-radio-list"})
        self.fields['bind_type'].widget.attrs.update({'class': "custom-radio-list"})
        self.fields['color'].widget.attrs.update({'class': "custom-radio-list"})
        #self.fields['message'].widgets.attrs.update({'class':'form-control'})
    

class ViewOrderForm(ModelForm):

    PRINT_TYPE=[('1','One side'),('2','Two side')]
    BIND_TYPE=[('1','Claims'),('2','Soft'),('3','Spiral')]
    COLOR = [('1','Color'), ('2','Black-White')]

    userID = forms.CharField(disabled=True)
    orderCode = forms.CharField(disabled=True)
    title = forms.FileField()
    print_type = forms.ChoiceField(choices=PRINT_TYPE, widget=forms.RadioSelect, disabled=True)
    bind_type = forms.ChoiceField(choices=BIND_TYPE, widget=forms.RadioSelect, disabled=True)
    number_of_copies = forms.IntegerField(disabled=True)
    color = forms.ChoiceField(choices=COLOR, widget=forms.RadioSelect, disabled=True)
    created_at = forms.DateTimeField(disabled=True)
    message = forms.CharField(disabled=True, widget=forms.Textarea(attrs={'placeholder':'Message'}))
    
    class Meta:
        model = Order
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(ViewOrderForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['userID'].disabled=True

        self.fields['orderCode'].widget.attrs.update({'placeholder': 'Order code'})
        self.fields['number_of_copies'].widget.attrs.update({'placeholder': 'Number of copies'})
        self.fields['print_type'].widget.attrs.update({'class': "custom-radio-list"})
        self.fields['bind_type'].widget.attrs.update({'class': "custom-radio-list"})
        self.fields['color'].widget.attrs.update({'class': "custom-radio-list"})
        self.fields['message'].widget.attrs.update({'placeholder': 'Message'})




class CreateUserForm(UserCreationForm):
    phoneNumber = CharField()

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['phoneNumber'].widget.attrs.update({'class': 'form-control'})

        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})


class ContactForm(forms.Form):
    error_css_class = 'error'

    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Your name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Your email'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Message'}))

    fields = ['name','email','message']


    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name == 'Your name':
            raise forms.ValidationError("Enter your name!")
        return name

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['message'].widget.attrs.update({'class': 'form-control'})



class ViewContactForm(ModelForm):

    name = forms.CharField(disabled = True)
    email = forms.EmailField(disabled=True)
    message = forms.CharField(widget=forms.Textarea,disabled=True)

    class Meta:
        model = ContactUsForm
        fields = ['name', 'email','message']
    
    def __init__(self, *args, **kwargs):
        super(ViewContactForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['message'].widget.attrs.update({'class': 'form-control'})


class CustomUserForm(forms.Form):
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    phoneNumber = forms.CharField()
    
    fields = ['username','first_name','last_name','email','phoneNumber']

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control','readonly':True})
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['phoneNumber'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs["onchange"]="changeWelcomeTitle()"

class CustomUserFormForAdmin(forms.Form):
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    phoneNumber = forms.CharField()
    
    fields = ['username','first_name','last_name','email','phoneNumber']

    def __init__(self, *args, **kwargs):
        super(CustomUserFormForAdmin, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control','readonly':True})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control','readonly':True})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control','readonly':True})
        self.fields['email'].widget.attrs.update({'class': 'form-control','readonly':True})
        self.fields['phoneNumber'].widget.attrs.update({'class': 'form-control','readonly':True})


class ChangePassword(PasswordChangeForm):
    old_password = forms.CharField(label='Old password', widget=forms.PasswordInput)

    fields = ['old_password', 'new_password1', 'new_password2']

    old_password.widget.attrs.update({'autocomplete':'off', 'maxlength':'32'})

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    
    
    fields = ['username', 'password']
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        
