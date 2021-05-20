from django.db import models

from django.contrib.auth.models import User


class CustomUser(models.Model):
    
    customuser = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phoneNumber = models.CharField(max_length=9, blank=True)
   

    def __str__(self):
        return f'{self.customuser.first_name} {self.customuser.last_name} ({self.customuser.username})'
    
    def save(self, *args, **kwargs):
        super(CustomUser, self).save(*args, **kwargs)


class Order(models.Model):
    userID = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE)
    orderCode = models.CharField(max_length=15, blank=False)
    title = models.FileField(upload_to='media')
    print_type = models.CharField(max_length=10)
    bind_type = models.CharField(max_length=10)
    number_of_copies = models.IntegerField()
    color = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=False)
    

    class Meta:  
        db_table = "printStudioApp_order"

    def __str__(self):
        return f'{self.orderCode}'


class ContactUsForm(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(unique=False)
    message = models.CharField(max_length=500)

    def __str__(self):
        return f'{self.name}'  
