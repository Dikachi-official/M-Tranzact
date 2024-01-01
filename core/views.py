from django.shortcuts import get_object_or_404, render
import json
import uuid
from django.contrib import messages, auth
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from userauth.models import User, Support
from account.models import Account, Kyc
from notifications_app import *
from .models import *
from .forms import KycRegistrationForm, EditKycRegistrationForm
from django.contrib.auth.models import Group
from .decorators import group_required


#FOR CELERY INTEGRATION
from django.shortcuts import HttpResponse
from channels.layers import get_channel_layer
from asgiref.sync  import async_to_sync

# Create your views here.

#To check if its working
def test(request):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notification_broadcast",
        {
            'type': 'send_notification',
            'message': json.dumps("Notification")
        }
    )
    return HttpResponse("Done")





def celery_mail(request):
    return HttpResponse("Done")



def welcome(request):        
    return render(request, 'interfaces/home.html')





@login_required
def dashboard(request):
    #KYC CHECKER TO RETURN MESSAGE
    try:
        kyc = Account.objects.get(user=request.user)
        if kyc.kyc_submitted == True:
            messages.success(request, "Kyc completed")
        else:
            group = Group.objects.get(name="Kyc_Unregistered")
            request.user.groups.add(group)
            messages.warning(request, "Please complete your Kyc registration to get full access")    
    except:       
         messages.warning(request, "Please complete your Kyc registration")       


    #GET THE USER
    user = User.objects.get(username=request.user)
    if request.method == "POST":
        form = KycRegistrationForm(request.POST, request.FILES or None)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            image = form.cleaned_data['image']
            marital_status = form.cleaned_data['marital_status']
            id_card = form.cleaned_data['id_card']
            gender = form.cleaned_data['gender']
            date_of_birth = form.cleaned_data['date_of_birth']
            signature = form.cleaned_data['signature']
            country = form.cleaned_data['country']
            state = form.cleaned_data['state']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            id_select = form.cleaned_data['id_select']

            #CREATE KYC INSTANCE
            user_kyc = Kyc.objects.create(
                user = user,
                full_name = full_name,
                image = image,
                marital_status = marital_status,
                id_select = id_select,
                id_card = id_card,
                gender = gender,
                date_of_birth = date_of_birth,
                signature = signature,
                country = country,
                state = state,
                city = city,
                mobile = mobile,
            )

            #CREATE ACCOUNT INSTANCE
            user_acct = Account.objects.create(
                user = request.user,
                account_status = "True",
                kyc_submitted = "True",
                kyc_confirmed = "True",
            )

            #CREATE CREDIT CARD INSTANCE
            user_card = CreditCard.objects.create(
                user = request.user,
                name = full_name,
                card_status = "True"
            )

            user_kyc.save()
            user_acct.save()
            user_card.save()
            group = Group.objects.get(name="Kyc_Registered")
            request.user.groups.add(group)
            #delete=Kyc.objects.all().delete()
            messages.success(request, f"Hey {request.user} Kyc has been successful")
            return redirect('core:dashboard')
        
    
    else:
        form = KycRegistrationForm()
    
    try:
        user_kyc = Kyc.objects.get(user=request.user)
        user_acct = Account.objects.get(user=request.user)

    except:
        user_kyc = None
        user_acct = None

    context = {
        "form": form,
        "user_kyc" :user_kyc,
        "user_acct" : user_acct,
        'room_name' : 'broadcast'
    }     
    
    #user_kyc = Kyc.objects.filter(user=request.user)
    
    return render(request, "interfaces/dashboard.html", context)





#TO DELETE ACCOUNT
@login_required
def delete_acct(request, id):
    account = get_object_or_404(Account, account_id=id, user=request.user)
    account.delete()
    return redirect("core:dashboard")





#CHECK USERS IN A GROUP
def AddToKycRegistered(request):
    group = Group.objects.get(name="Kyc_Registered")
    request.user.groups.add(group)
    return redirect('core:dashboard')




@login_required
def balance (request):
    if request.user.groups.filter(name = "Kyc_Registered").exists():

        #GETTING TRANSACTION LIST OF A PARTICULAR USER
        transactions = Transaction.objects.filter(user=request.user)
        received_transactions = Transaction.objects.filter(receiver=request.user)
        transact = Transaction.objects.filter(user=request.user)

        #GETTING THE BALANCE OF A PARTICULAR USER
        card_owner = CreditCard.objects.get(user=request.user)
        try:
            user_kyc = Kyc.objects.get(user=request.user)
            user_acct = Account.objects.get(user=request.user)

        except:
            user_kyc = None
            user_acct = None

        context = {
            "transactions": transactions,
            "received_transactions": received_transactions,
            'transact':transact,
            "card_owner" : card_owner,
            "user_kyc" :user_kyc,
            "user_acct" : user_acct
        }
        return render(request, "interfaces/balance.html", context)
    else:
        messages.warning(request, 'complete Kyc to continue')
        return redirect('core:dashboard')  




# TO INITIATE TRANSFER
@login_required
def transfer1 (request):
    if request.user.groups.filter(name = "Kyc_Registered").exists():
        if request.method == "POST":
            account_number = request.POST.get('acct_no')

            #GET THE ACCOUNT AND IMAGE
            try:
                account=Account.objects.get(account_number=account_number)
                user_img = Kyc.objects.get(user=account.user)
            except:
                messages.warning(request, "Account doesn't exist")
                return redirect('core:transfer1')
            
            try:
                user_kyc = Kyc.objects.get(user=request.user)
                user_acct = Account.objects.get(user=request.user)
            except:
                user_kyc = None
                user_acct = None    
   
            context = {
                "account": account,
                "user_kyc" :user_kyc,
                "user_acct" : user_acct,
                "user_img" : user_img
            } 
            
            return render(request, "interfaces/pay1.html", context)

        try:
            user_kyc = Kyc.objects.get(user=request.user)
            user_acct = Account.objects.get(user=request.user)
        except:
            user_kyc = None
            user_acct = None


        context = {
            "user_kyc" :user_kyc,
            "user_acct" : user_acct,
        }
        return render(request, "interfaces/pay1.html", context)


    else:
        messages.warning(request, 'complete Kyc to continue')
        return redirect('core:dashboard')





# TO TRANSFER TO DESTINATION ACCOUNT
@login_required
def transfer2 (request, id):
    if request.user.groups.filter(name = "Kyc_Registered").exists():
        if request.method == "POST":
            #amount = float(request.POST.get('amount'))
            amount = request.POST.get('amount')
            description = request.POST.get('description')
            pin = request.POST.get('pin')

            
            # GET RECIEVERS ACCOUNT TO PASS ID FOR TRANSACTION 
            dest_account = Account.objects.get(id=id)
            #GET ACCOUNT ID FOR ROUTE REDIRECTION
            redirect_id = Account.objects.get(id=dest_account.id)


            source_acct = Account.objects.get(user = request.user)
            #GET SENDERS PIN
            pin_number=source_acct.pin_number

               
            try:
                amount = float(amount)
                if source_acct.account_balance >= amount:
                        
                    if pin == pin_number:
                        #VERIFY PIN
                        source_acct.account_balance -= amount
                        dest_account.account_balance += amount

                        source_acct.save()
                        dest_account.save()   
                    else:
                        messages.warning(request, " Incorrect PIN")
                        return redirect('core:transfer2', id=redirect_id)  
                    
                    if amount <= 0:
                        messages.error(request, "Amount too low")
                        return redirect('core:transfer2', id=redirect_id)
                        
                    #SAVE THIS TRANSACTION TO DATABASE
                    transact = Transaction.objects.create(
                        user = source_acct.user,# must be a user instance
                        amount = amount,
                        status="completed",
                        transfer_type="transfer",
                        receiver = dest_account.account_number,
                        sender = source_acct.account_number, #must be a charfield
                        description = description or "Transfer",
                    )
                    transact.save()
                    messages.success(request, "Transfer Successful")
                    return redirect("core:transfer-successful")
                    
                else:
                    messages.warning(request, "Insufficient Funds")
                    return redirect('core:transfer2', id=redirect_id)
                

            except (ValueError, TypeError):
                        messages.error(request, "Input must be a valid number") 
                        return redirect('core:transfer2', id=redirect_id)   
                

        try:
            user_kyc = Kyc.objects.get(user=request.user)
            user_acct = Account.objects.get(user=request.user)
            dest_account = Account.objects.get(account_id=id)
            target = dest_account.user
            receiver = Kyc.objects.get(user=target)

        except:
            user_kyc = None
            user_acct = None

        context = {
            "user_kyc" :user_kyc,
            "user_acct" : user_acct,
            "dest_account": dest_account,
            "receiver": receiver
        }

        return render(request, "interfaces/pay2.html", context)
    else:
        messages.warning(request, 'complete Kyc to continue')
        return redirect('core:dashboard')





@login_required
def deposit(request):
    #CHECKING IF USER EXISTS IN GROUP
    if request.user.groups.filter(name = "Kyc_Registered").exists():
        user = Account.objects.get(user=request.user)
        #LOGIC TO DEPOSIT FUNDS
        if request.method == "POST":
            account_number = request.POST.get('acct_no')
            amount = request.POST.get('amount')
            description = request.POST.get('description')

            #QUERY 
            try:
                account_number = int(account_number)
                amount = float(amount)
                if account_number > 0 and amount > 0: 
                    try:
                        account=Account.objects.get(account_number = account_number)      
                        account.account_balance += amount
                        account.save()
                        transaction = Transaction.objects.create(
                                user = request.user,
                                amount = amount,
                                status="completed",
                                transfer_type="deposit",
                                receiver = account_number,
                                sender = user.user.username,
                                description = description or "Deposit",
                                )
                        transaction.save()
                        messages.success(request, 'Deposited successfully')
                        return redirect('core:deposit')    
                    except Account.DoesNotExist:
                        messages.error(request, "Account doesn't exist")
                        return redirect('core:deposit')
                           
                else:
                    messages.warning(request, "Invalid account number, Please enter valid values")
                    return redirect('core:deposit') 
            
            # Handle the case where the input is empty or only white space
            except ValueError:
                messages.warning(request, "Invalid input, Please enter valid numbers")
                return redirect('core:deposit')


        try:
            user_kyc = Kyc.objects.get(user=request.user)
            user_acct = Account.objects.get(user=request.user)

        except:
            user_kyc = None
            user_acct = None

            
        context ={
            "user_kyc" :user_kyc,
            "user_acct" : user_acct
        }             
        return render(request, "interfaces/deposit.html", context) 
    else:
        messages.warning(request, 'complete Kyc to continue')
        return redirect('core:dashboard')




@login_required
def withdraw(request):
    #CHECKING IF USER EXISTS IN GROUP
    if request.user.groups.filter(name = "Kyc_Registered").exists(): 
        user = Account.objects.get(user=request.user)
        #LOGIC TO WITHDRAW FUNDS
        if request.method == "POST":
            account_number = request.POST.get('acct_no')
            amount = request.POST.get('amount')
            description = request.POST.get('description')
            pin = request.POST.get('pin')

            #GET USERS PIN
            source_acct = Account.objects.get(user = request.user)
            user_acct_no=source_acct.account_number
            pin_number=source_acct.pin_number

            #QUERY 
            try:
                account_number = int(account_number)
                amount = float(amount)
                if account_number > 0 and amount > 0:
                    if pin == pin_number:
                        try:
                            account=Account.objects.get(account_number = account_number)
                            if account.account_number == user_acct_no:
                                if account.account_balance >= amount:
                                    account.account_balance -= amount
                                    account.save()
                                    messages.success(request, 'Withdrawal successfully')
                                    transaction = Transaction.objects.create(
                                        user = request.user,
                                        amount = amount,
                                        status="completed",
                                        transfer_type="withdrawal",
                                        receiver = account_number,
                                        sender = user.user.username,
                                        description = description or "Withdrawal",
                                    )
                                    transaction.save()
                                    return redirect('core:withdraw')
                                else:
                                    messages.warning(request, "Insufficient Funds")
                                    return redirect('core:withdraw')
                            else:
                                messages.warning(request, "Wrong account number, Please input your account number")
                                return redirect('core:withdraw')

                        except Account.DoesNotExist:
                            messages.warning(request, "Account doesn't exist")
                            return redirect('core:withdraw')
                    else:
                        messages.warning(request, " Incorrect PIN")
                        return redirect("core:withdraw")     
                else:
                    messages.warning(request, "Invalid account number, Please enter valid values")
                    return redirect('core:withdraw') 
            except ValueError:
                messages.warning(request, "Invalid input, Please enter valid numbers")
                return redirect('core:withdraw')   
        
        try:
            user_kyc = Kyc.objects.get(user=request.user)
            user_acct = Account.objects.get(user=request.user)

        except:
            user_kyc = None
            user_acct = None

            
        context ={
            "user_kyc" :user_kyc,
            "user_acct" : user_acct
        }      
        return render(request, "interfaces/withdraw.html", context)        
    
    else:
        messages.warning(request, 'complete Kyc to continue')
        return redirect('core:dashboard') 






#TRANSFER SUCCESSFUL
def transfer_success(request):
    #CHECKING IF USER EXISTS IN GROUP
    if request.user.groups.filter(name = "Kyc_Registered").exists(): 
     



        try:
                user_kyc = Kyc.objects.get(user=request.user)
                user_acct = Account.objects.get(user=request.user)

        except:
            user_kyc = None
            user_acct = None

            
        context ={
            "user_kyc" :user_kyc,
            "user_acct" : user_acct
        } 
        return render(request, "interfaces/transfer_success.html", context)

    else:
        messages.warning(request, 'complete Kyc to continue')
        return redirect('core:dashboard')




    

# SUPPORT VIEW
def support(request):
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
    return render(request, "interfaces/support.html", context)

def ajax_contact_form(request):
    # USING JAVASCRIPT FORMAT
    full_name = request.GET['full_name']
    email = request.GET['email']
    phone = request.GET['phone']
    subject = request.GET['subject']
    message = request.GET['message']

    contact = Support.objects.create(
        full_name = full_name,
        email = email,
        phone = phone,
        subject = subject,
        message = message
    )

    data = {
        "bool":True,
        "message": "Message sent successfully..."
    }

    return JsonResponse({"data":data})  





# SETTINGS VIEW
def settings(request):
    #CHECKING IF USER EXISTS IN GROUP
    if request.user.groups.filter(name = "Kyc_Registered").exists(): 
            
        #TO EDIT PROFILE AT PROFILE SETTINGS
        #GET THE USER
        user = User.objects.get(username=request.user)

        if request.method == "POST":
            form = EditKycRegistrationForm(request.POST, request.FILES or None, instance=user)
            if form.is_valid():
                user_details = Kyc.objects.get(user=request.user)
                user_details.delete()


                # GET UPDATED DETAILS
                full_name = form.cleaned_data['full_name']
                image = form.cleaned_data['image']
                marital_status = form.cleaned_data['marital_status']
                id_card = form.cleaned_data['id_card']
                gender = form.cleaned_data['gender']
                date_of_birth = form.cleaned_data['date_of_birth']
                signature = form.cleaned_data['signature']
                country = form.cleaned_data['country']
                state = form.cleaned_data['state']
                city = form.cleaned_data['city']
                mobile = form.cleaned_data['mobile']
                id_select = form.cleaned_data['id_select']

                #CREATE KYC INSTANCE
                user_kyc = Kyc.objects.create(
                    user = user,
                    full_name = full_name,
                    image = image,
                    marital_status = marital_status,
                    id_select = id_select,
                    id_card = id_card,
                    gender = gender,
                    date_of_birth = date_of_birth,
                    signature = signature,
                    country = country,
                    state = state,
                    city = city,
                    mobile = mobile,
                )
                user_kyc.save()
                form.save()
                messages.success(request, "Uploaded successfully")
                return redirect('core:settings')
        else:
            user_details = Kyc.objects.get(user=request.user)
            form = EditKycRegistrationForm(instance=user_details)
        



        try:
            user_kyc = Kyc.objects.get(user=request.user)
            user_acct = Account.objects.get(user=request.user)

        except:
            user_kyc = None
            user_acct = None

            
        context ={
            "user_kyc" :user_kyc,
            "user_acct" : user_acct,
            "form":form,
        } 

        return render(request, "interfaces/settings.html", context)

    else:
        messages.warning(request, 'complete Kyc to continue')
        return redirect('core:dashboard')