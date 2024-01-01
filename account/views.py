from django.shortcuts import get_object_or_404, render
import json
import uuid
from django.contrib import messages, auth
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from userauth.models import User
from core.models import *
from .models import *
from core.forms import KycRegistrationForm
from django.contrib.auth.models import Group
from core.decorators import group_required


# Create your views here.
@login_required
def stat_gen (request):
    if request.user.groups.filter(name = "Kyc_Registered").exists():

        #GETTING TRANSACTION LIST OF A PARTICULAR USER
        user_acct = Account.objects.get(user=request.user)
        transactions = Transaction.objects.filter(user=request.user)
        received_transactions = Transaction.objects.filter(receiver=user_acct.account_number)
        
       
        try:
            user_kyc = Kyc.objects.get(user=request.user)
            user_acct = Account.objects.get(user=request.user)

        except:
            user_kyc = None
            user_acct = None

        context = {
            "transactions": transactions,
            "received_transactions": received_transactions,
            "user_kyc" :user_kyc,
            "user_acct" : user_acct
        }

        return render(request, "interfaces/stat_of_acct.html", context)    
    else:
        messages.warning(request, 'complete Kyc to continue')
        return redirect('core:dashboard')



@login_required
def stat_detail(request, id):
    if request.user.groups.filter(name = "Kyc_Registered").exists():

        #GETTING TRANSACTION OF A PARTICULAR USER
        transaction = Transaction.objects.get(id=id)

        #GETTING THE BALANCE OF A PARTICULAR USER
        card_owner = CreditCard.objects.filter(user=request.user)
        try:
            user_kyc = Kyc.objects.get(user=request.user)
            user_acct = Account.objects.get(user=request.user)

        except:
            user_kyc = None
            user_acct = None

        context = {
            "transaction": transaction,
            "card_owner" : card_owner,
            "user_kyc" :user_kyc,
            "user_acct" : user_acct
        }

        return render(request, "interfaces/stat_acct_detail.html", context)    
    else:
        messages.warning(request, 'complete Kyc to continue')
        return redirect('core:dashboard')


#REGISTER A BILL THROUGH ECS
@login_required
def ecs(request):
    if request.user.groups.filter(name = "Kyc_Registered").exists():
        user_acct = Account.objects.get(user=request.user)
        if request.method == "POST":
            name = request.POST.get('name')
            acctno = request.POST.get('accno')
            upper_limit = request.POST.get('upper_limit')

            #CHECK THE ACCOUNT THAT CORRESPONDS WITH COLLECTED
            try:
                acc_obj = Account.objects.get(account_number = acctno)
            except:
                messages.warning(request, "Account number doesn't exist")
                return redirect("account:ecs")

            ecs = ECS_Data.objects.create(
                user = request.user,
                payer = name,
                upper_limit = upper_limit,
                account = acc_obj
            )
            bill = Bills.objects.create(
                user = request.user,
                amount = upper_limit,
            )

            ecs.save()
            bill.save()
            messages.success(request, "Data uploaded successfully to bills")
            return redirect("account:ecs")
            
        try:
            user_kyc = Kyc.objects.get(user=request.user)
            user_acct = Account.objects.get(user=request.user)

        except:
            user_kyc = None
            user_acct = None

        context = {
            "user_kyc" :user_kyc,
            "user_acct" : user_acct
        } 

        return render(request, "interfaces/ecs.html", context)
    else:
        messages.warning(request, 'complete Kyc to continue')
        return redirect('core:dashboard')
    




#LIST OUT BILLS FOR THE USER
@login_required
def bills(request):
    if request.user.groups.filter(name = "Kyc_Registered").exists():
        ecs = ECS_Data.objects.filter(user=request.user)
        bills = Bills.objects.filter(user=request.user, completed=False)
        

        try:
            user_kyc = Kyc.objects.get(user=request.user)
            user_acct = Account.objects.get(user=request.user)

        except:
            user_kyc = None
            user_acct = None

        context = {
            "user_kyc" :user_kyc,
            "user_acct" : user_acct,
            "ecs":ecs,
            "bills":bills
        } 

        return render(request, "interfaces/bills.html", context)
    else:
        messages.warning(request, 'complete Kyc to continue')
        return redirect('core:dashboard')
    


#PAY A BILL FOR A USER
@login_required
def Pay_bills(request, id):
    if request.user.groups.filter(name = "Kyc_Registered").exists():
        ecs = ECS_Data.objects.get(ecs_id=id)
        upper_limit=ecs.upper_limit
        receiver=ecs.account
        collector = Account.objects.get(account_id=receiver)
        collect=collector.user.username

        # DEBIT FROM USER
        source_acct = Account.objects.get(user = request.user)
        if source_acct.account_balance >= upper_limit:
            source_acct.account_balance -= upper_limit

            source_acct.save()

            #SAVE THIS TRANSACTION TO DATABASE
            transact = Transaction.objects.create(
                user = source_acct.user,# must be a user instance
                amount = upper_limit,
                status="completed",
                transfer_type="transfer",
                receiver = collect,
                sender = source_acct.account_number, #must be a charfield
                description = "ECS clearance",
            )
            transact.save()  

            bill = Bills.objects.create(
                amount = upper_limit,
                completed="True"      
            )
            bill.save()

            #DELETE THAT RECOARD AFTER PAYMENT MADE
            ecs = get_object_or_404(ECS_Data, ecs_id=id, user=request.user)
            ecs.delete()

            messages.success(request, 'Bill Paid Successfully')
            return redirect("account:bills")
        else:
            messages.warning(request, "Insufficient Funds")
            return redirect("account:bills")    
 
    else:
        messages.warning(request, 'complete Kyc to continue')
        return redirect('core:dashboard')
