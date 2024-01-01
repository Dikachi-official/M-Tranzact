# Generated by Django 4.1.2 on 2023-10-08 01:18

from django.db import migrations
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_ecs_data_bills'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_number',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='123456789', length=8, max_length=10, prefix='23', unique=True),
        ),
    ]
