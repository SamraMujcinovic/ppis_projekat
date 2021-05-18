# Generated by Django 3.2.3 on 2021-05-18 18:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('printStudioApp', '0002_alter_customuser_phonenumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='bind_type',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='order',
            name='color',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='number_of_copies',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='print_type',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='order',
            name='userID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL),
        ),
    ]