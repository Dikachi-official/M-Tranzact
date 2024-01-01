from django.shortcuts import render
import json
import uuid
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse

#MY USER IMPORTS
from account.models import Account, Kyc
from .forms import RegistrationForm
from .models import User


#EMAIL ACTIVATION IMPORTS
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .tokens import account_activation_token   
from django.core.mail import EmailMessage  


# IMPORT FOR CHANGE PASSWORD FUNCTION
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash



# Create your views here.

#EMAIL ACTIVATION WITH TOKEN VIEW
def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
        
    if user is not None and account_activation_token.check_token(user, token):   
        user.is_active = True
        user.save()  

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')  
        return redirect("userauth:signin")
    else:  
        messages.warning(request, 'Activation link is invalid!')
        return redirect("userauth:signup") 



'''
# TO ACTIVATE THE USER EMAIL AND HANDLE ERRORS ALONG
def activateEmail(request, user, to_email):
    mail_subject = "Activate your account"
    message = render_to_string("activate_account.html", {
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f"Dear <b>{user}</b>, Please go to your email <b>{email}</b> inbox and click on \received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.")
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')

'''


# REGISTER VIEW
def register_view(request):
    if request.user.is_authenticated:
        messages.warning(
            request, f"Hey {request.user} you are already logged in.")
        return redirect('core:home')

    if request.method == 'POST':
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            
            '''
            # LETS OMIT THE EMAIL ACTIVATION TO AVOID ERRRORS
            current_site = get_current_site(request)
            mail_subject = "Activation link has been sent to your email"
            message = render_to_string('activate_account.html',{
                'user':user,
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            #activateEmail(request, user, form.cleaned_data.get('email'))
            '''
            messages.success(request, f"Hey {user.username}, your account was created successfully. Please login to continue")
            return redirect('userauth:signin')


            '''
            new_user = form.save()
            # WE USE CLEANED DATA TO FETCH ALL VALUES FROM THE REQUEST
            firstname = form.cleaned_data['firstname']
            messages.success(
                request, f'Hey {firstname}, Your account was created successfully')

            #new_user = authenticate(email=form.cleaned_data['email'], 
                                    #password=form.cleaned_data['password1'])
            login(request, new_user)

            #Profile.objects.create(user=request.user)

            return redirect('core:dashboard')
            '''
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)    
    else:
        form = RegistrationForm()

    context = {
        'form': form
    }
    return render(request, "authentication/register.html", context)





#LOGIN VIEW
def login_view(request):
    if request.user.is_authenticated:
        messages.warning(
            request, f"Hey {request.user} you are already logged in.")
        return redirect('core:home')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email)
        except:
            messages.warning(request, f"User with {email} doesn't exists ☹")    
            return redirect('userauth:signin')
        
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            print(user.firstname)
            
            messages.success(request, "You are now logged in")
            return redirect("core:home")
            
        else:
            messages.error(request, "User does not exist ☹, create an account.")
            return redirect('userauth:signup')
    return render(request, "authentication/login.html")




#LOGOUT
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out')
    return redirect('core:home')




#CHANGE PASSWORD
@login_required(login_url='login')
def change_password(request):
    #CHECKING IF USER EXISTS IN GROUP
    if request.user.groups.filter(name = "Kyc_Registered").exists(): 
        if request.method == "POST":
            form=PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, "Your password has been changed successfully....")
                return redirect("core:settings")
        else:
            form = PasswordChangeForm(user=request.user)
        
        try:
            user_kyc = Kyc.objects.get(user=request.user)
            user_acct = Account.objects.get(user=request.user)

        except:
            user_kyc = None
            user_acct = None

        context ={
            'form':form,
            "user_kyc" :user_kyc,
            "user_acct" : user_acct
        }    

        return render(request, "authentication/change_password.html", context)
    
    else:
        messages.warning(request, 'complete Kyc to continue')
        return redirect('core:dashboard') 