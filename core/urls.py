from django.urls import path
from . import views


app_name = "core"

urlpatterns = [
    # HOME PAGE
    path('', views.welcome, name="home"),

    # CELERY MAIL
    path('mail/', views.celery_mail, name="mail"),

    #DASHBOARD
    path('dashboard', views.dashboard, name="dashboard"),

    #DELETE ACCOUNT
    path('delete-account/<str:id>/', views.delete_acct, name="delete-acct"),

    #ADD TO KYC REGITERED
    path('AddToKycRegistered', views.AddToKycRegistered, name="AddToKycRegistered"),

    #BALANCE AND TRANSACTIONS
    path('balance', views.balance, name="balance"),

    #MAKE PAYMENT STEP1
    path('transfer1', views.transfer1, name="transfer1"),

    #MAKE PAYMENT STEP2
    path('transfer2/<str:id>/', views.transfer2, name="transfer2"),

    #TRANSFER SUCCESSFUL
    path('transfer-successful', views.transfer_success, name="transfer-successful"),

    #MAKE DEPOSIT TO YOUR ACCOUNT
    path('deposit', views.deposit, name="deposit"),

    #MAKE WITHDRAWALS FROM ACCOUNT
    path('withdraw', views.withdraw, name='withdraw'),

    #SUPPPORT/ CONTACT US
    path('support/helpdesk', views.support, name="support"),
    path('ajax-contact-form/', views.ajax_contact_form, name="ajax-contact-form"),


    #SETTINGS AND PRIVACY
    path('settings/', views.settings, name="settings"),
]