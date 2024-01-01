from django.urls import path
from core import views
from core.views import test


app_name = "notification"

urlpatterns = [
    # NOTIFICATION TEST
    path('test/', views.test, name='test')
]