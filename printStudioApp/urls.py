from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),  
    path('logout/', views.logoutUser, name="logout"),

    path('adminn/', views.adminPage, name="adminn"),

    path('customer/', views.customerPage, name="customer"),
    path('userProfile/<int:pk>', views.userProfilePage, name="userProfile"),
    path('userProfileForAdmin/<int:pk>', views.userProfilePage, name="userProfileForAdmin"),
    url(r'^password/$', views.change_password, name='change_password'),

    path('order/', views.orderPage, name="order"),
    path('viewOrder/<int:pk>', views.viewOrderPage, name="viewOrder"),

    path('contactForm/', views.contactUsFormPage, name="contactForm"),
    path('viewContactDetails/<int:pk>', views.viewContactDetailsPage, name="viewContactDetails"),

    path('', views.home, name="home"),
]