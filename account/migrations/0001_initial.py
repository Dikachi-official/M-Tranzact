# Generated by Django 4.1.2 on 2023-10-03 02:15

import account.models
from django.db import migrations, models
import django.db.models.deletion
import shortuuid.django_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_id', shortuuid.django_fields.ShortUUIDField(alphabet='123456789', length=6, max_length=8, prefix='01', unique=True)),
                ('account_number', shortuuid.django_fields.ShortUUIDField(alphabet='123456789', length=8, max_length=10, prefix='02', unique=True)),
                ('account_balance', models.IntegerField(default=0)),
                ('pin_number', models.IntegerField(default=1234)),
                ('account_status', models.BooleanField(default=False)),
                ('kyc_submitted', models.BooleanField(default=False)),
                ('kyc_confirmed', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Kyc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=200, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=account.models.user_directory_path)),
                ('marital_status', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=100)),
                ('id_card', models.ImageField(upload_to='image')),
                ('date_of_birth', models.DateTimeField()),
                ('signature', models.ImageField(upload_to='image')),
                ('country', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('mobile', models.IntegerField()),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='kyc_account', to='account.account')),
            ],
        ),
    ]
