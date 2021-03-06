import re
from django.shortcuts import render, redirect 
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


# Create your views here.
from .models import *
from .forms import  ChangePassword, CustomUserForm, OrderForm, CreateUserForm, ContactForm, ViewOrderForm, ViewContactForm, CustomUserFormForAdmin

from .decorators import unauthenticated_user, admin_only, allowed_users
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from printStudioApp.functions import handle_uploaded_file
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.core.files import File
from os.path import basename
from urllib.request import urlretrieve, urlcleanup
from urllib.parse import urlsplit

from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import message, send_mail, BadHeaderError
from rest_framework import viewsets


def registerPage(request):

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            firstname= form.cleaned_data.get('first_name')
            lastname= form.cleaned_data.get('last_name')
            emailvalue= form.cleaned_data.get('email')
            usernameForm = form.cleaned_data.get('username')
            passwordForm = form.cleaned_data.get('password1')
            phoneNumberForm = form.cleaned_data.get('phoneNumber')

            userExists = User.objects.filter(email=request.POST.get('email'))
            userExists_list = list(userExists)
            if len(userExists_list) != 0:
                messages.error(request, 'Profile with email '+emailvalue+' already exists!', extra_tags='emailExists')
                form = CreateUserForm()
                context = {'form':form}
                return redirect('register')
            else:
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

def validateEmail( email ):
    
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False

def loginPage(request):
    if request.method == 'POST':
        print("uslo u login")
        
        usernameForm = request.POST.get('username')
        password =request.POST.get('password')
        print(request.POST)
            
        user = authenticate(request, username=usernameForm, password=password)
            
        if user is not None:
            login(request, user)
            group = None
            if user.groups.exists():
                group = user.groups.all()[0].name
            
            #if group=='admin':
             #   return redirect('adminn')
            #elif group=='customer':
             #   return redirect('customer')
            #else:
             #   return HttpResponse('You are not authorized to view this page')
            return HttpResponseRedirect('/userProfile/%d'%request.user.id)
        else:
            okMail = validateEmail(usernameForm)
            if okMail:
                usernamefromMail = User.objects.get(email__exact=usernameForm)
                user = authenticate(request, username=usernamefromMail.username, password=password)
                if user is not None:
                    login(request, user)
                    group = None
                    if user.groups.exists():
                        group = user.groups.all()[0].name
                        return HttpResponseRedirect('/userProfile/%d'%request.user.id)
                else:
                    messages.error(request, 'Username/email OR password is incorrect', extra_tags='incorrectusername')

            else:
                messages.error(request, 'Username/email OR password is incorrect', extra_tags='incorrectusername')

    context = {}
    return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')


@unauthenticated_user
@login_required(login_url='login')
@admin_only
def adminPage(request):
    orders = Order.objects.all().order_by('-created_at')

    customers = CustomUser.objects.all()
    
    total_customers = customers.count()
    
    total_orders = orders.count()

    contacts = ContactUsForm.objects.all()


    context = {'orders':orders, 'customers':customers,
	'total_orders':total_orders,'total_customers':total_customers,'contacts':contacts }
    
    return render(request, 'admin.html', context)


@unauthenticated_user
@login_required(login_url='login')
@allowed_users(['customer','admin'])
def customerPage(request):
    customuserModel = CustomUser.objects.get(pk=request.user.id)
    phone = customuserModel.phoneNumber
    my_orders = Order.objects.filter(userID=request.user)
    my_contactForms = ContactUsForm.objects.filter(email=request.user.email)

    context = {'my_orders':my_orders, 'my_contactForms':my_contactForms,
	'user':request.user,'phone':phone }
    
    return render(request, 'customer.html', context)

@unauthenticated_user
@login_required(login_url='login')
@allowed_users(['customer','admin'])
def userProfilePage(request, *args, **kwargs):
    form = CustomUserForm()
    method = request.POST.get('_method', '').lower()
    selectedCustomer = None
    search = kwargs.get('pk')
    if(request.user.pk != search and request.user.groups.all()[0].name != "admin" or User.objects.filter(pk=search).exists()==False):
        return HttpResponse('You are not authorized to view this page')

    if method == 'post':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            
            
            if search:
                selectedCustomer = CustomUser.objects.filter(pk=search)
                selectedCustomer_list = list(selectedCustomer)
                selectedCustomer = selectedCustomer_list[0]
            
            usernameForm = form.cleaned_data.get('username')
            
            firstnameForm = form.cleaned_data.get('first_name')
            lastnameForm = form.cleaned_data.get('last_name')
            emailForm= form.cleaned_data.get('email')
            phoneNumberForm= form.cleaned_data.get('phoneNumber')
            
            userWithEmail = list(User.objects.filter(email=request.POST.get('email')))[0]
            print(userWithEmail.username)
            if userWithEmail.username == usernameForm:
                try:
                    user, created = User.objects.update_or_create(pk=search,defaults={'first_name':firstnameForm, 'last_name':lastnameForm, 'email':emailForm,'username':usernameForm})
                    my_group = Group.objects.get(name='customer') 
                    my_group.user_set.add(user)
                    user.save()
                    customer, created = CustomUser.objects.update_or_create(pk=search, defaults={'customuser':user,'phoneNumber': phoneNumberForm})
                    customer.save()
                    
                    messages.success(request, 'User updated successfully!!')
                    return redirect('userProfile')
                except:
                    form = CustomUserForm({'username':selectedCustomer.customuser.username,'first_name':selectedCustomer.customuser.first_name,'last_name':selectedCustomer.customuser.last_name,'email':selectedCustomer.customuser.email,'password':selectedCustomer.customuser.password,'phoneNumber':selectedCustomer.phoneNumber})
                    context = {'form':form}
                    return render(request, 'userProfile.html', context)
            else:
                userWithUsername = User.objects.filter(username=request.POST.get('username'))
                userWithUsername_list = list(userWithUsername)
                if len(userWithUsername_list) != 0:
                    messages.error(request, 'User with username ' +request.POST.get('username')+' already exists!!', extra_tags='alreadyExists')
                    form = CustomUserForm({'username':selectedCustomer.customuser.username,'first_name':selectedCustomer.customuser.first_name,'last_name':selectedCustomer.customuser.last_name,'email':selectedCustomer.customuser.email,'password':selectedCustomer.customuser.password,'phoneNumber':selectedCustomer.phoneNumber})
                    context = {'form':form}
                    return render(request, 'userProfile.html', context)
                else:
                    try:
                        user, created = User.objects.update_or_create(pk=search,defaults={'first_name':firstnameForm, 'last_name':lastnameForm, 'email':emailForm,'username':usernameForm})
                        my_group = Group.objects.get(name='customer') 
                        my_group.user_set.add(user)
                        user.save()
                        customer, created = CustomUser.objects.update_or_create(pk=search, defaults={'customuser':user,'phoneNumber': phoneNumberForm})
                        customer.save()
                        
                        messages.success(request, 'User updated successfully!!')
                        return redirect('userProfile')
                    except:
                        form = CustomUserForm({'username':selectedCustomer.customuser.username,'first_name':selectedCustomer.customuser.first_name,'last_name':selectedCustomer.customuser.last_name,'email':selectedCustomer.customuser.email,'password':selectedCustomer.customuser.password,'phoneNumber':selectedCustomer.phoneNumber})
                        context = {'form':form}
                        return render(request, 'userProfile.html', context)
                
    else:
        if request.user.is_authenticated:
            search = kwargs.get('pk')
            if search:
                selectedCustomer = CustomUser.objects.filter(pk=search)
                selectedCustomer_list = list(selectedCustomer)
                selectedCustomer = selectedCustomer_list[0]
                print(selectedCustomer)
            if request.user.groups.all()[0].name == "admin" and request.user.username != selectedCustomer.customuser.username:
                form = CustomUserFormForAdmin()
                print(request)
                form = CustomUserFormForAdmin({'username':selectedCustomer.customuser.username,'first_name':selectedCustomer.customuser.first_name,'last_name':selectedCustomer.customuser.last_name,'email':selectedCustomer.customuser.email,'password':selectedCustomer.customuser.password,'phoneNumber':selectedCustomer.phoneNumber})
                context = {'form':form}
                print(form)
                return render(request, 'viewUserForAdmin.html', context)
            else:
                form = CustomUserForm()
                print(request)
                search = kwargs.get('pk')
                if search:
                    selectedCustomer = CustomUser.objects.filter(pk=search)
                    selectedCustomer_list = list(selectedCustomer)
                    selectedCustomer = selectedCustomer_list[0]
                    print(selectedCustomer)
                    form = CustomUserForm({'username':selectedCustomer.customuser.username,'first_name':selectedCustomer.customuser.first_name,'last_name':selectedCustomer.customuser.last_name,'email':selectedCustomer.customuser.email,'password':selectedCustomer.customuser.password,'phoneNumber':selectedCustomer.phoneNumber})
                    context = {'form':form}
                    print(form)
                    return render(request, 'userProfile.html', context)
            

    context = {'form':form}
    return render(request, 'customer.html', context)       

def home(request):
    
    return render(request, 'home.html', {})

def about(request):
    
    return render(request, 'about.html', {})


@unauthenticated_user
@login_required(login_url='login')
@allowed_users(['customer','admin'])
def orderPage(request):
    
    form = OrderForm()

    if request.method == 'POST':
        print("uslo u post u order")
        form = OrderForm(request.POST,request.FILES)
        if form.is_valid():
            print("uslo u post u order valid")

            userOrder = request.user
            orderCode = form.cleaned_data.get('orderCode')
            
            title = request.FILES['title']
            print_type = form.cleaned_data.get('print_type')
            bind_type = form.cleaned_data.get('bind_type')
            number_of_copies = form.cleaned_data.get('number_of_copies')
            color = form.cleaned_data.get('color')
            created_at = timezone.localtime(timezone.now())
            message = form.cleaned_data.get('message')
            
            orderForm = Order.objects.create(userID=userOrder, orderCode=orderCode, title=title,print_type=print_type,bind_type=bind_type,number_of_copies=number_of_copies,color=color,created_at=created_at, message=message)
            orderForm.save()
            messages.success(request, 'Order made successfully!', extra_tags='orderMade')
            if request.user.is_authenticated:
                return HttpResponseRedirect('/userProfile/%d'%request.user.id)
            return redirect('home')

    context = {'form':form}
    return render(request, 'order.html', context)

def download(request,path):
    file_path=os.path.join(settings.MEDIA_ROOT,path)
    if os.path.exists(file_path):
        with open(file_path,'rb')as fh:
            response=HttpResponse(fh.read(),content_type="application/adminupload")
            response['Content-Disposition']='inline;filename='+os.path.basename(file_path)
            return response
    raise Http404	

@unauthenticated_user
@login_required(login_url='login')
@allowed_users(['customer','admin'])
def viewOrderPage(request, *args, **kwargs):
    form = ViewOrderForm()
    method = request.POST.get('_method', '').lower()
    search = kwargs.get('pk')
    my_orders = Order.objects.filter(userID=request.user)
    ok = False
    for i in range(len(my_orders)):
        if my_orders[i].pk == search:
            ok=True

    if(ok == False and request.user.groups.all()[0].name != "admin" or Order.objects.filter(pk=search).exists()==False):
        return HttpResponse('You are not authorized to view this page')

    if method == 'delete':
            search = kwargs.get('pk')
            if search:
                selectedOrder = Order.objects.filter(pk=search).delete()
                messages.success(request, 'Order deleted successfully!', extra_tags='orderDeleted')
                return redirect('listOrders')
    else:
        if request.user.is_authenticated:
            search = kwargs.get('pk')
            if search:
                selectedOrder = Order.objects.filter(pk=search)
                selectedOrder_list = list(selectedOrder)
                selectedOrder = selectedOrder_list[0]
                userOrder = list(User.objects.filter(pk=selectedOrder.userID.pk))[0]
                form = ViewOrderForm(instance=selectedOrder, initial={'userID':userOrder.username})
                #form.fields['title'].widget = forms.HiddenInput()
                context = {'form':form}
                return render(request, 'viewOrder.html', context)

    context = {'form':form}

    return render(request, 'viewOrder.html', context)

def contactUsFormPage(request):
    print(request.POST)
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            print("uslo u formu")
            nameForm = form.cleaned_data.get('name')
            emailForm= form.cleaned_data.get('email')
            messageForm= form.cleaned_data.get('message')
            created_at = timezone.localtime(timezone.now())
            
            contactForm = ContactUsForm.objects.create(name=nameForm, email=emailForm, message=messageForm, created_at=created_at)
            contactForm.save()
            messages.success(request, 'Message sent successfully!', extra_tags='sentContact')
            if request.user.is_authenticated:
                return HttpResponseRedirect('/userProfile/%d'%request.user.id)
            return redirect('home')

    else:
        if request.user.is_authenticated:
            form = ContactForm(initial={'name': request.user.first_name, 'email': request.user.email})
            context = {'form':form}
            return render(request, 'contactUsForm.html', context)
        else:
            form = ContactForm()
            context = {'form':form}
            return render(request, 'contactUsForm.html', context)

    context = {'form':form}
    return render(request, 'contactUsForm.html', context)       

@unauthenticated_user
@login_required(login_url='login')
@allowed_users(['customer','admin'])
def viewContactDetailsPage(request, *args, **kwargs):
    form = ViewContactForm()
    method = request.POST.get('_method', '').lower()
    search = kwargs.get('pk')
    my_contactForms = list(ContactUsForm.objects.filter(email=request.user.email))
    ok = False
    for i in range(len(my_contactForms)):
        if my_contactForms[i].pk == search:
            ok=True

    if(ok == False and request.user.groups.all()[0].name != "admin" or ContactUsForm.objects.filter(pk=search).exists()==False):
        return HttpResponse('You are not authorized to view this page')

    if method == 'delete':
            search = kwargs.get('pk')
            if search:
                selectedContact = ContactUsForm.objects.filter(pk=search).delete()
                messages.success(request, 'Contact form deleted successfully!', extra_tags='contactDeleted')
                return redirect('listContactForms')
    else:
        if request.user.is_authenticated:
            search = kwargs.get('pk')
            if search:
                selectedContact = ContactUsForm.objects.filter(pk=search)
                selectedContact_list = list(selectedContact)
                selectedContact = selectedContact_list[0]
                form = ViewContactForm(instance=selectedContact)
                context = {'form':form}
                return render(request, 'viewContactDetails.html', context)
        

    context = {'form':form}
    return render(request, 'viewContactDetails.html', context)       

def change_password(request, *args, **kwargs):
    search = kwargs.get('pk')
    if request.method == 'POST':
        form = ChangePassword(request.user, request.POST)
        print(form)
        if form.is_valid():
            passwordForm = form.cleaned_data.get('new_password1')
            user, created = User.objects.update_or_create(pk=search,defaults={'password':passwordForm})

            user.set_password(passwordForm)
            user.save()
            
            selectedcustomer, created = CustomUser.objects.update_or_create(pk=search, defaults={'customuser':user})
            selectedcustomer.save()            
            #update_session_auth_hash(request, user)  
            messages.success(request, 'Your password was successfully updated!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        print("user old pass")
        print(request.user.password)
        form = ChangePassword(request.user)
        print(form)
    return render(request, 'password_change_form.html', {
        'form': form
    })

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                    "email":user.email,
                    'domain':'localhost:8000',
                    'site_name': 'Print Studio App',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'smujcinovi1@etf.unsa.ba' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                    return redirect ('password_reset_done')
    
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})

@unauthenticated_user
@login_required(login_url='login')
@allowed_users(['customer','admin'])
def listOrders(request):
    context = {}
    orders = Order.objects.all().order_by('-created_at')

    if request.user.groups.all()[0].name == "admin":
        context = {'orders': orders }
    else:
        my_Orders = Order.objects.filter(userID = request.user.pk).order_by('-created-at')
        context = {'orders':my_Orders }

    return render(request, 'listOrders.html', context)


@unauthenticated_user
@login_required(login_url='login')
@admin_only
def listCustomers(request):
    context = {}
    
    customers = CustomUser.objects.all()

    context = {'customers':customers }
    
    return render(request, 'listCustomers.html', context)


@unauthenticated_user
@login_required(login_url='login')
@allowed_users(['customer','admin'])
def listContactForms(request):
    context = {}

    contacts = ContactUsForm.objects.all().order_by('-created_at')

    if request.user.groups.all()[0].name == "admin":
        context = {'contacts': contacts }
    else:
        my_contactForms = ContactUsForm.objects.filter(email=request.user.email).order_by('-created_at')
        context = {'contacts':my_contactForms }


    return render(request, 'listContactForms.html', context)
