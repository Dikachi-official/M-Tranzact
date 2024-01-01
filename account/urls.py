from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    #ELECTRONIC CLEARANCE SERVICE
    path('ecs/bills', views.ecs, name="ecs"),

    #BILLS PAYMENT
    path('bills', views.bills, name="bills"),
    path('pay_bills/<str:id>', views.Pay_bills, name="pay-bills"),
    

    #STATEMENT OF ACCOUNT
    path('statement_amount', views.stat_gen, name="statements"),
    path('statement/<str:id>', views.stat_detail, name="statement")
]