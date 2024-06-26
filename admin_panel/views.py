from django.shortcuts import render,redirect
import pyrebase
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime
import random
import time
import string
from django.contrib import messages

# Create your views here.
firebaseconfig = {
     "apiKey": "AIzaSyAqAg8PTWJSPXEsjeOOLPx-SiT0WOvnCIA",
     "authDomain": "traffic-memo-system-b842c.firebaseapp.com",
     "databaseURL": "https://traffic-memo-system-b842c-default-rtdb.firebaseio.com",
     "projectId": "traffic-memo-system-b842c",
     "storageBucket": "traffic-memo-system-b842c.appspot.com",
     "messagingSenderId": "985582841078",
     "appId": "1:985582841078:web:08c7c00ea65f2dd06210d7",
     "measurementId": "G-JQ5TKGP6CN"
}
dict1=[]
firebase=pyrebase.initialize_app(firebaseconfig)
auth=firebase.auth()
db=firebase.database()
def admin(request):
    if 'email' not in request.session:
        return redirect('/login')
    
    else:
          data=db.child('memos').get()
          dataval=data.val()
          keys = dataval.keys()
          dict1 = []
          context=dict()
          sendData=dict()
          for key in keys:
               sendData[key]=dataval[key]
          context["memos"]=sendData
          for key in keys:
               if dataval[key]['roadnm']=="nehrunagar":
                    listdata=[
                         dataval[key]['dateandtime'],
                         dataval[key]['email'],
                         dataval[key]['fine'],
                         dataval[key]['imageurl'],
                         dataval[key]['name'],
                         dataval[key]['pdfurl'],
                         dataval[key]['plateno'],
                         dataval[key]['roadnm'],
                         dataval[key]['speed']
                    ]
                    dict1.append(listdata)
          print(dict1)         
    
    return render(request=request,template_name='admin.html',context=context)

def login(request): 
    global email1,password1
    if request.method=="POST":
        data=request.POST
        email1=data['email']
        password1=data['password']
        var=sendmail()
        if var==1:
             return redirect('/system-admin/send_verification')

        
    return render(request,"login.html")
    
            

def sendmail():
        global otp,roadnm,email,password
        from_email = 'generativegenz@gmail.com'
        password = 'fzpp lciy sndd mado'
        subject="One Time Password For Admin "
        length=8
        alphanumeric_characters = string.ascii_letters + string.digits
        otp=''.join(random.choice(alphanumeric_characters) for _ in range(length))
        otp=otp.upper()
        print(otp)
        body=f"""

        <h1 style="text-align:center">One Time Password For Sign-in</h1>

        <p>Thank you for registering on our admin panel. To complete the registration process, please use the following One-Time Password (OTP)</p>

        <h2>Your OTP : {otp}</h2>

        <p>
        Please enter this OTP on the registration page to verify your identity and activate your account.

        If you did not initiate this registration, please ignore this message.

        </p>

        Thank you,
        <br>
        Government Of India.

        """
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = email1
        msg.attach(MIMEText(body, 'html'))


        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, email1, msg.as_string())
            print("OTP Send Successfully")
            
        return 1

       

def verify(request):
     global roadnm
     if request.method=="POST":
          data=request.POST
          otp_entered=data['otp']
          data=db.child('admin').get()
          data2=data.val()
          for key,data_items in data2.items():
               if data_items['email']==email1:
                    name=data_items['name']
                    roadnm=data_items['roadnm']
                    role=data_items['role']

          issignin=auth.sign_in_with_email_and_password(email1,password1)


          if otp_entered==otp and issignin is not None:
               request.session['email']=email1
               request.session['roadnm']=roadnm
               request.session['name']=name
               request.session['role']=role
               print("Login Successful")
               

               messages.success(request,"Login Successfully")

               if role=="staff":    
                    return redirect('/system-admin/home')
               elif role=="admin":
                    return redirect('/super-admin/home')

               

          else:
               messages.error(request,"Login Unsucessfully")
               return redirect('/system-admin/login')
               
     return render(request,"verify.html")


def logout(request):
    if 'email' in request.session:
        request.session.pop('email')
        request.session.pop('role')
        request.session.pop('name')
        request.session.pop('roadnm')
        return redirect('/login')

def reqPswdChng(request):
    return render(request,"reqPasswordChange.html")
