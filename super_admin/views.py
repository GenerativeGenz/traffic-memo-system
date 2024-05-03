from django.shortcuts import render,redirect
import pyrebase

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
db=firebase.database()

# Create your views here.
def index(request):
    if 'email' not in request.session:
        return redirect('/login')
    
    context = {
        "title":"Dashboard"
    }
    return render(request=request,template_name="dashboard.html",context=context)

def pswdChange(request):
    return render(request=request,template_name='pswdChange.html')

def memoView(request):
    roadway_filter = request.GET.get('roadwayFilter', '')
    vehicle_type_filter = request.GET.get('vehicleTypeFilter', '')
    name_plate_filter = request.GET.get('namePlateFilter', '')
    data=db.child('memos').get()
    dataval=data.val()
    context=dict()
    sendData=dict()
    keys=dataval.keys()
    for key in keys:
        sendData[key]=dataval[key]
    # context["memos"]=sendData
    context = {
        'memos': sendData,
        'roadway_filter': roadway_filter,
        'vehicle_type_filter': vehicle_type_filter,
        'name_plate_filter': name_plate_filter,
    }
    print("context[memos] : ", context["memos"])
    return render(request=request, template_name='memoView.html', context=context)

def userDetails(request):
    data=db.child('users').get()
    dataval=data.val()
    context=dict()
    sendData=dict()
    keys=dataval.keys()
    for key in keys:
        sendData[key]=dataval[key]
    context["users"]=sendData
    return render(request=request,template_name='userDetails.html',context=context)


def login(request):
    return render(request,"login.html")

def staff(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        road = request.POST.get('road')
        role = request.POST.get('role')
        # print(name, email, password, road, role)
        data = {"name":name, "email":email, "password":password, "roadnm":road, "role":role}
        db.child("admin").push(data)
    context=dict()
    data=db.child('admin').get()
    dataval=data.val()
    sendData=dict()
    keys=dataval.keys()
    for key in keys:
        sendData[key]=dataval[key]
    context["staffs"]=sendData
    # print(context)
    return render(request,"staffDetails.html",context=context)