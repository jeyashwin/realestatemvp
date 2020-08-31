#user views
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.models import User,auth
from .models import USER,LANDLORD
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect

import uuid


# Create your views here.

def decoding(obj):
    return eval(obj.decode())

# @csrf_exempt
# def register(request):
#     print("validating")
#     if request.method == "POST":
#         request = decoding(request.body)
#         first_name = request["first_name"]
#         last_name = request["last_name"]
#         password1 = request["password1"]
#         password2 = request["password2"]
#         email = request["email"]
#         user = User.objects.create_user(username=uuid.uuid4().hex[:8],password=password1,email=email,first_name = first_name,
#                                         last_name = last_name)
#         user.save()
#     return JsonResponse({"Success" : 1})


def signin(request):
    if request.method == "GET":
        print("gotcha",dir(request),)
    return JsonResponse({"got" : 1})

@csrf_exempt
@csrf_protect
def register(request):
    if request.method == "POST":
        if request.POST["usertype"] == "buyer":
            first_name = request.POST["fname"]
            last_name = request.POST["lname"]
            password = request.POST["pass"]
            email = request.POST["email"]
            birth_date = request.POST["dob"]
            college = request.POST["college"]
            user = USER(user_id=uuid.uuid4().hex[:8],password=password,email_id=email,first_name = first_name,
                                            last_name = last_name,college = college,birth_date = birth_date)
            user.save()
            return render(request,"templates/index.html",{"status" : 1})
        elif request.POST["usertype"] == "seller":
            first_name = request.POST["fname"]
            last_name = request.POST["lname"]
            password = request.POST["pass"]
            email = request.POST["email"]
            birth_date = request.POST["dob"]
            print(first_name, last_name, birth_date, password, email)
            ld = LANDLORD(l_id=uuid.uuid4().hex[:8], password=password, email_id=email, first_name=first_name,
                        last_name=last_name, birth_date=birth_date)
            ld.save()
            return render(request,"templates/index.html",{"status" : 1})
    else:
        return render(request, "templates/index.html", {"status": 0})

@csrf_protect
@csrf_exempt
def login(request):
    if request.method == "POST":
        print("Entered")
        # request1 = decoding(request.body)
        email_id = request.POST['email']
        password = request.POST['pass']
        print(email_id,password)
        # email_id = request.POST['email']
        # password = request.POST['pass']
        try:
            user = USER.objects.get(email_id = email_id)
        except Exception as e:
            print(e,"Exception")
            user = None
        if user is not None:
            u_id = USER.objects.filter(email_id = email_id)
            resp = {"user_id" : [i.user_id for i in u_id][0],"fname" : [i.first_name for i in u_id][0]}
            return render(request, "templates/index.html",resp)
        else:
            return render(request,"templates/index.html",{"status" : 0})
