# Generated by Django 3.2.3 on 2021-05-29 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('printStudioApp', '0003_auto_20210518_1809'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='message',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='title',
            field=models.FileField(upload_to='media'),
        ),
        migrations.AlterModelTable(
            name='order',
            table='printStudioApp_order',
        ),
    ]