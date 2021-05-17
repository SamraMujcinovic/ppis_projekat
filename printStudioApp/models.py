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
    title = models.FileField(upload_to='documents')
    ONE_SIDE = 1
    TWO_SIDE = 2
    PRINT_TYPE = (
        (ONE_SIDE, 'one'),
        (TWO_SIDE, 'two')
    )

    print_type = models.PositiveSmallIntegerField(choices=PRINT_TYPE)

    CLAIMS = 1
    SOFT = 2
    SPIRAL = 3
    BIND_TYPE = (
        (CLAIMS, 'claims'),
        (SOFT, 'soft'),
        (SPIRAL, 'spiral')
    )

    bind_type = models.PositiveSmallIntegerField(choices=BIND_TYPE)

    number_of_copies = models.PositiveIntegerField()

    COLOR = 1
    WB = 2
    COLOR_TYPE = (
        (COLOR, 'color'),
        (WB, 'white-black')
    )
    color = models.PositiveSmallIntegerField(choices=COLOR_TYPE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}. {self.userID.username}'


class ContactUsForm(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(unique=False)
    message = models.CharField(max_length=500)

    def __str__(self):
        return f'{self.id}. {self.name}'  
