from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),  
    path('logout/', views.logoutUser, name="logout"),
    path('adminn/', views.adminPage, name="adminn"),
    path('customer/', views.customerPage, name="customer"),
    path('order/', views.orderPage, name="order"),
    path('contactForm/', views.contactUsFormPage, name="contactForm"),
   
    path('', views.home, name="home"),
]