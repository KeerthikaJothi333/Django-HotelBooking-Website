from django.urls import path
from .views import (
    CustomLoginView, CustomRegisterView)
from . import views

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='signin'),
    path('register/', CustomRegisterView.as_view(), name='signup'),
    # path('sendtestemail/', send_mail_page),

    # Password Reset URLs
    path('send-otp/', views.send_otp_email, name='send-otp'),
    path('verify-otp/', views.verify_otp, name='verify-otp'),
    path('set-new-password/', views.set_new_password, name='set-new-password'),

]
