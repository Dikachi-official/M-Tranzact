from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import uuid # TO USE UUID
from shortuuid.django_fields import ShortUUIDField
from userauth.models import User

# Create your models here.

GENDER_CHOICES = (
    ("male", "Male"),
    ("female", "Female")
)

MARITAL_CHOICES = (
        ("single", "Single"),
        ("marrried", "Married")
    )

IDENTITY_CHOICES = (
        ("national id card", "National ID Card"),
        ("drivers licence", "Drivers Licence"),
        ("international passport", "International Passport")
    )

def user_directory_path(instance, filename):
    return 'user_(0)/(1)'.format(instance.user.id, filename)


class Account(models.Model):
    account_id = ShortUUIDField(unique=True, length=6, max_length=8,prefix="01", alphabet="123456789")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="account_owner")
    account_number = ShortUUIDField(unique=True, length=8, max_length=10,prefix="23", alphabet="123456789")
    account_balance = models.IntegerField(default=0)
    pin_number = ShortUUIDField(unique=True, length=3, max_length=4,prefix="1", alphabet="123456789")
    account_status = models.BooleanField(default=False)
    kyc_submitted = models.BooleanField(default=False)
    kyc_confirmed = models.BooleanField(default=False)
    #recommended_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="recommender")
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return self.account_id


class Kyc(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="kyc_owner")
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True, related_name="kyc_account")
    full_name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    marital_status = models.CharField(choices=MARITAL_CHOICES, max_length=13, null=True, blank=True)
    id_select = models.CharField(choices=IDENTITY_CHOICES, max_length=25, null=True, blank=True)
    id_card = models.ImageField(null=True, blank=True, upload_to="image")
    gender = models.CharField(choices=GENDER_CHOICES, max_length=13, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    signature = models.ImageField(null=True, blank=True, upload_to="image")
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name
    


class ECS_Data(models.Model):
    ecs_id = ShortUUIDField(unique=True, length=16, max_length=16, alphabet="123456789")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="ecs_owner")
    payer = models.CharField(max_length=300)
    upper_limit = models.FloatField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True, related_name="ecs_account")
    
    def __str__(self):
        return self.payer
    
    class Meta:
        verbose_name_plural = "Ecs_data"
    
class Bills(models.Model):
    #id column created implicitly
    bill_id = models.ForeignKey(ECS_Data, on_delete=models.CASCADE, null=True, blank=True,)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="bill_owner")
    amount = models.FloatField()
    completed = models.BooleanField(default = False)
    

    class Meta:
        verbose_name_plural = "Bills"     