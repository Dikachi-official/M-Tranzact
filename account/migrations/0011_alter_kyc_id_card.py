# Generated by Django 4.1.2 on 2023-10-05 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_alter_kyc_id_card'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kyc',
            name='id_card',
            field=models.ImageField(default='', upload_to='img'),
        ),
    ]
