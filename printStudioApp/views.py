import re
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm

from .decorators import unauthenticated_user, admin_only, allowed_users
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


def registerPage(request):
    
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            # form.save()
            firstname= form.cleaned_data.get('first_name')
            lastname= form.cleaned_data.get('last_name')
            emailvalue= form.cleaned_data.get('email')
            usernameForm = form.cleaned_data.get('username')
            passwordForm = form.cleaned_data.get('password1')
            phoneNumberForm = form.cleaned_data.get('phoneNumber')
            user = User.objects.create_user(first_name=firstname, last_name=lastname, email=emailvalue,username=usernameForm,password=passwordForm)
            user.set_password(user.password)
            my_group = Group.objects.get(name='customer') 
            my_group.user_set.add(user)
            customer = CustomUser.objects.create(customuser=user,phoneNumber = phoneNumberForm)
            customer.save()
            messages.success(request, 'Account was created for ' + customer.customuser.username)
            return redirect('login')

    context = {'form':form}
    return render(request, 'register.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')
            
        user = authenticate(request, username=username, password=password)
            
        if user is not None:
            login(request, user)
            group = None
            if user.groups.exists():
                group = user.groups.all()[0].name
            
            if group=='admin':
                return redirect('adminn')
            elif group=='customer':
                return redirect('customer')
            else:
                return HttpResponse('You are not authorized to view this page')

        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')


@unauthenticated_user
@login_required(login_url='login')
@admin_only
def adminPage(request):
  
    #provjeri da li je admin
    orders = Order.objects.all()
    customers = CustomUser.objects.all()
    
    total_customers = customers.count()
    
    total_orders = orders.count()

    contacts = ContactUsForm.objects.all()

    context = {'orders':orders, 'customers':customers,
	'total_orders':total_orders,'total_customers':total_customers,'contacts':contacts }
    
    return render(request, 'admin.html', context)


@unauthenticated_user
@login_required(login_url='login')
@allowed_users(['customer'])
def customerPage(request):
    customuserModel = CustomUser.objects.get(pk=request.user.id)
    phone = customuserModel.phoneNumber
    my_orders = Order.objects.filter(userID=request.user)
    my_contactForms = ContactUsForm.objects.filter(email=request.user.email)

    context = {'my_orders':my_orders, 'my_contactForms':my_contactForms,
	'user':request.user,'phone':phone }
    
    return render(request, 'customer.html', context)


def home(request):
    
    return render(request, 'home.html', {})