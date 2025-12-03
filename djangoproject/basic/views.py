from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import connection
import json
from django.views.decorators.csrf import csrf_exempt
from basic.models import Student,Users
from django.contrib.auth.hashers import make_password,check_password
import jwt
from django.conf import settings
from datetime import datetime,timedelta 
from zoneinfo import ZoneInfo 



def func(request):
    return HttpResponse("Hello Director")

def sample(request):
    return HttpResponse("hello world")

def sample1(request):
    return HttpResponse("Welcome to Django")

def sampleinfo(request):
    # data={"name":'Krishna','age':25,'city':'hyderabad'}
    data={"result":[4,6,8,9]}
    return JsonResponse(data,safe=False)

def dynamicResponse(request):
    name=request.GET.get("name",'Krishna')
    city=request.GET.get("city",'hyd')
    return HttpResponse(f"Hello {name} from {city}")

def add(request):
    # get two numbers from the query parameters (URL)
    num1 = request.GET.get('a', 0)
    num2 = request.GET.get('b', 0)

    try:
        # convert them to integers and calculate sum
        total = int(num1) + int(num2)
        return HttpResponse(f"The sum of {num1} and {num2} is {total}")
    except ValueError:
        return HttpResponse("Please enter valid numbers!")

# to test database connection
def health(request):
        try:
            with connection.cursor() as c:
                c.execute("SELECT 1")
            return JsonResponse({"status":"ok","db":"connected"})
        except Exception as e:
            return JsonResponse({"status":"error","db":str(e)})
          

@csrf_exempt
def addStudent(request):
    print(request.method)
    if request.method=="POST":
        data=json.loads(request.body)
        student=Student.objects.create(
            name=data.get('name'),
            age=data.get("age"),
            email=data.get("email")
            ) 
        return JsonResponse({"status":"success","id":student.id},status=200)
    elif request.method=="GET":
        # data=json.loads(request.body)
        ref=request.GET.get("id")
        result=Student.objects.filter(id=ref).values().first()
        print(result)
        return JsonResponse({"status":"ok","data":result},status=200)
    

    elif request.method=="PUT":
        data=json.loads(request.body)
        ref_id=data.get("id")
        new_email=data.get("email")
        exsistinng_student=Student.objects.get(id=ref_id)
        # print(exsistinng_student)
        exsistinng_student.email=new_email
        exsistinng_student.save()
        updated_data=Student.objects.filter(id=ref_id).values().first()
        print(updated_data)
        return JsonResponse({"status":"Data Updated successfully","updated_data":updated_data},status=200)
    


    elif request.method=="DELETE":
        data=json.loads(request.body)
        ref_id=data.get("id")
        student=Student.objects.filter(id=ref_id).values().first()
        print(student)
        student_new=Student.objects.filter(id=ref_id)
        student_new.delete()
        return JsonResponse({"req":"delete method requested"},status=200)
    return JsonResponse({"error":"use post method"},status=400)


@csrf_exempt
def job1(request):
    return JsonResponse({"message":"u have successfully applied for job1"},status=200)
def job2(request):
    return JsonResponse({"message":"u have successfully applied for job2"},status=200)


@csrf_exempt
def signUp(request):
    if request.method=="POST":
        data=json.loads(request.body)
        print(data)
        user=Users.objects.create(
            username=data.get('username'),
            email=data.get('email'),
            password=make_password(data.get('password'))
        )
    return JsonResponse({"status":"success","data":user.username},status=200)  

@csrf_exempt
def login(request):
    if request.method=="POST":
        data=request.POST
        print(data)
        username=data.get("username")
        password=data.get("password")
        try:
            user=Users.objects.get(username=username)
            issued_time=datetime.now(ZoneInfo("Asia/Kolkata"))
            expired_time=issued_time+timedelta(minutes=1)
            if check_password(password,user.password):
                # token="a json web token"
                payload={"username":user.username,"email":user.email,"id":user.id,"exp":expired_time}
                token=jwt.encode(payload,settings.SECRET_KEY,algorithm="HS256")
                return JsonResponse({"status":"successfully logged in",'token':token,"issued_at":issued_time,"expired_in":(expired_time-issued_time).total_seconds()/60},status=200)
            else:
                return JsonResponse({"status":"failed","message":"invalid password"},status=400)
        except Users.DoesNotExist:
            return JsonResponse({"status":"failure","message":"user not found"},status=400)

@csrf_exempt
def change_password(request):
    if request.method == "POST":

        data = request.POST
        username = data.get("username")
        old_password = data.get("old_password")
        new_password = data.get("new_password")

        # Check username exists
        try:
            user = Users.objects.get(username=username)
        except Users.DoesNotExist:
            return JsonResponse({"status":"error","message":"User not found"}, status=400)

        # Verify old password
        if not check_password(old_password, user.password):
            return JsonResponse({"status":"error","message":"Old password incorrect"}, status=400)

        # Hash and update new password
        user.password = make_password(new_password)
        user.save()

        return JsonResponse({"status":"success","message":"Password updated successfully"}, status=200)

    return JsonResponse({"error":"Only POST method allowed"}, status=400)


@csrf_exempt
def check(request):
    hashed="pbkdf2_sha256$870000$FUeZFjKTu0TqhEcP4xE88T$fYSFN77RkVnp57/xj80C6H6WyGrdIpS4vwPASAYqDnw="
    ipdata=request.POST
    print(ipdata)
    # hashed=make_password(ipdata.get("ip"))
    x=check_password(ipdata.get("ip"),hashed)
    print(x)
    return JsonResponse({"status":"success","data":x},status=200)

@csrf_exempt
def getAllUsers(request):
    if request.method=="GET":
        users=list(Users.objects.values())
        print(request.token_data,"token data in view")
        print(request.token_data.get("username"))
        print(users,"users'list")
        for user in users:
            if user["username"] == request.token_data.get("username"):
                return JsonResponse({"status":"success","loggedinuser":request.token_data,"data":users},status=200)  
        else:    
            return JsonResponse({"error":"Unauthorized access"},status=401)
    