from django.contrib import admin
from django.urls import path
from admin_panel import views

urlpatterns = [
   path('home',view=views.admin,name='admin'),
   path('',views.login,name="login"),
   path('send_verification',views.verify,name="verification"),
   path('sendmail',views.sendmail,name="sendmail"),
   path('verify',views.verify,name="verify"),
   path('login',views.login,name="login"),
   path('logout',views.logout,name="logout"),
   path('request-password-change',views.reqPswdChng,name="passwordChange"),
]