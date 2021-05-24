from django.urls import path
from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),  
    path('logout/', views.logoutUser, name="logout"),

    path('adminn/', views.adminPage, name="adminn"),

    path('customer/', views.customerPage, name="customer"),
    path('userProfile/<int:pk>', views.userProfilePage, name="userProfile"),
    path('userProfileForAdmin/<int:pk>', views.userProfilePage, name="userProfileForAdmin"),
    path('change_password/<int:pk>', views.change_password, name="change_password"),

    path('order/', views.orderPage, name="order"),
    path('viewOrder/<int:pk>', views.viewOrderPage, name="viewOrder"),

    path('contactForm/', views.contactUsFormPage, name="contactForm"),
    path('viewContactDetails/<int:pk>', views.viewContactDetailsPage, name="viewContactDetails"),

    path("password_reset", views.password_reset_request, name="password_reset"),

    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('listOrders/', views.listOrders, name="listOrders"),
    path('listCustomers/', views.listCustomers, name="listCustomers"),
    path('listContactForms/', views.listContactForms, name="listContactForms"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)