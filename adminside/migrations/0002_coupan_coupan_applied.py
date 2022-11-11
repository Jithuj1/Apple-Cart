# Generated by Django 4.0.6 on 2022-10-28 06:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('adminside', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupan_code', models.CharField(max_length=25)),
                ('start_date_and_time', models.DateTimeField()),
                ('end_date_and_time', models.DateTimeField()),
                ('discount_amount', models.CharField(blank=True, max_length=5)),
                ('discount_percentage', models.CharField(blank=True, max_length=5)),
                ('maximum_usage', models.IntegerField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Coupan_applied',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminside.coupan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]