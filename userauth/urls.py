from django.urls import path
from . import views


app_name = "userauth"

urlpatterns = [
    #SIGN UP PAGE
    path('signup', views.register_view, name="signup"),

    #LOGIN PAGE
    path('signin', views.login_view, name="signin"),

    #LOGOUT PAGE
    path('signout', views.logout, name='signout'),

    #EMAIL ACTIVATION VERIFICATION
    path('activate/<uidb64>/<token>', views.activate, name='activate'),

    #CHANGE PASSWORD
    path('changepassword/', views.change_password, name='change-password'),


]