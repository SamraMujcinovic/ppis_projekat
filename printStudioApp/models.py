from django.db import models

from django.contrib.auth.models import User


class CustomUser(models.Model):
    
    customuser = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phoneNumber = models.CharField(max_length=9, blank=True)
    #roles = models.ManyToManyField(Role)

    def __str__(self):
        return f'{self.customuser.id}. {self.customuser.first_name} {self.customuser.last_name}'


class Order(models.Model):
    userID = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE)
    orderCode = models.CharField(max_length=15, blank=False)
    title = models.FileField()
    print_type = models.CharField(max_length=10)
    bind_type = models.CharField(max_length=10)
    number_of_copies = models.IntegerField()
    color = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:  
        db_table = "printStudioApp_order"

    def __str__(self):
        return f'{self.id}. {self.userID.username}'


class ContactUsForm(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(unique=False)
    message = models.CharField(max_length=500)

    def __str__(self):
        return f'{self.id}. {self.name}'  
