# Generated by Django 4.0.6 on 2022-10-31 05:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_product_data_discount_price'),
        ('adminside', '0004_categoryoffer'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_till', models.DateField()),
                ('Name', models.CharField(max_length=100)),
                ('percentage', models.IntegerField()),
                ('description', models.TextField()),
                ('status', models.BooleanField(default=True, max_length=20)),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.product_data')),
            ],
        ),
    ]
