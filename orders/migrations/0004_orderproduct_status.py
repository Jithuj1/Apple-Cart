# Generated by Django 4.0.6 on 2022-10-27 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='status',
            field=models.CharField(default='Delivered', max_length=50),
        ),
    ]
