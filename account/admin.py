from django.contrib import admin
from . models import *

# Register your models here.
class AccountAdmin(admin.ModelAdmin):
    list_editable = ['account_status','kyc_submitted','kyc_confirmed']
    list_display = ['user','pin_number', 'kyc_confirmed', 'account_number', 'account_balance']

class KycAdmin(admin.ModelAdmin):
    list_editable = ['date_of_birth','mobile']
    list_display = ['user','marital_status', 'gender']


admin.site.register(Account)
admin.site.register(Kyc)
admin.site.register(ECS_Data)
admin.site.register(Bills)
