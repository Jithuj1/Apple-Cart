# Generated by Django 4.0.6 on 2022-10-01 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(default=True, max_length=50),
        ),
    ]