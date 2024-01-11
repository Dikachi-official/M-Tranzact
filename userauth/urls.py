from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views


app_name = "userauth"

urlpatterns = [
    #SIGN UP PAGE
    path('signup', views.register_view, name="signup"),

    #LOGIN PAGE
    path('signin', views.login_view, name="signin"),

    #LOGOUT PAGE
    path('signout', views.logout, name='signout'),

    #EMAIL ACTIVATION VERIFICATION
    path("verify-email/<slug:username>", views.verify_email, name="verify-email"),
    path("resend-otp", views.resend_otp, name="resend-otp"),

    #CHANGE PASSWORD
    path('changepassword/', views.change_password, name='change-password'),


    # PASSWORD RESET URLS
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='authentication/password_reset_form.html', 
        email_template_name='authentication/password_reset_email.html',
        success_url=reverse_lazy('userauth:password_reset_done')), 
        name='password_reset'),
        
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='authentication/password_reset_done.html', ), name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='authentication/password_reset_confirm.html', 
        success_url=reverse_lazy('userauth:password_reset_complete', )), 
        name='password_reset_confirm'),

    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password_reset_complete.html', ), name='password_reset_complete'),





]