from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import uuid  # TO USE UUID
from shortuuid.django_fields import ShortUUIDField
from userauth.models import User

# Create your models here.

STATUS_CHOICE = (
    ("processing", "Processing"),
    ("completed", "Completed")
)

TRANSFER_TYPE = (
    ("transfer", "Transfer"),
    ("deposit", "Deposit"),
    ("withdrawal", "Withdrawal")
)

class Transaction(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="transactor")
    amount = models.IntegerField()
    status = models.CharField(choices=STATUS_CHOICE, max_length=13, default="processing")
    transfer_type = models.CharField(choices=TRANSFER_TYPE, max_length=10)
    receiver = models.CharField(max_length=200)
    sender = models.CharField(max_length=200)
    description = models.TextField(null=True, default="Transaction")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender


class CreditCard(models.Model):
    card_id = ShortUUIDField(unique=True, length=16, max_length=16, alphabet="123456789")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="card_owner")
    name = models.CharField(max_length=150)
    month = models.CharField(max_length=200, default=10)
    year = models.CharField(max_length=200, default=28 )
    cvv = ShortUUIDField(unique=True, length=3, max_length=3, alphabet="123456789")
    card_type = models.CharField(max_length=100, default="visa")
    card_status = models.BooleanField(default = False)

    def __str__(self):
        return self.name
    

