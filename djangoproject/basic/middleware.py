from django.http import JsonResponse
import re,json
from basic.models import Users

class sscMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self,request):
        if(request.path in ["/job1/","/job2/"]):
            ssc_result=request.GET.get("ssc")
            if(ssc_result!='True'):
                return JsonResponse({"error":"U should qualify atleast ssc for appplying this job"},status=400)
        return self.get_response(request)  
class MedicalfitMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self,request):
        if(request.path =="/job1/"): 
            medical_fit_result=request.GET.get("medically_fit")
            if(medical_fit_result!='True'):
                return JsonResponse({"error":"U not medically fit to apply for this job role"},status=400)   
        return self.get_response(request)
    
class AgeMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self,request):
        if(request.path in ["/job1/","/job2/"]):
            Age_checker=int(request.GET.get("age",17))
            if(not(18<=Age_checker<=25)):
                return JsonResponse({"error":"age must be in between 18 and 25"},status=400)
        return self.get_response(request)              
    

class UsernameMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self,request):
        if (request.path=="/signup/"):
            data=json.loads(request.body)
            username=data.get("username","")
            #checks username is empty or not
            if not username:
                return JsonResponse({"error":"username is required"},status=400)
            #checks length
            if len(username)<3 or len(username)>20:
             return JsonResponse({"error":"username should contains 3 to 20 characters"},status=400)
            #checks starting and ending
            if username[0] in "._" or username[-1] in "._":
             return JsonResponse({"error":"username should not starts or ends with . or _"},status=400)
            #checks allowed characters
            if not re.match(r"^[a-zA-Z0-9._]+$", username):
              return JsonResponse({"error":"username should contain letters,numbers,dot,underscore"},status=400)
            #checks .. and __
            if ".." in username or "__" in username:
             return JsonResponse({"error":"username cannot have .. or __"},status=400)
        return self.get_response(request)    
    


class EmailMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/signup/":
            data = json.loads(request.body)
            email = data.get("email", "")

            # 1. Check empty
            if not email:
                return JsonResponse({"error": "email is required"}, status=400)

            # 2. Basic email format check
            if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
                return JsonResponse({"error": "invalid email format"}, status=400)

            # 3. No ".." (consecutive dots)
            if ".." in email:
                return JsonResponse({"error": "email cannot contain consecutive dots"}, status=400)
            # 5. Check duplicate email
            if Users.objects.filter(email=email).exists():
                return JsonResponse({"error": "email already exists"}, status=400)

        return self.get_response(request)




class PasswordMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/signup/":
            data = json.loads(request.body)
            password = data.get("password", "")

            # Empty check
            if not password:
                return JsonResponse({"error": "password is required"}, status=400)

            # Length check
            if len(password) < 8 or len(password) > 20:
                return JsonResponse({"error": "password should contain 8 to 20 characters"}, status=400)

            # Strong password check (inline regex like your style)
            if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+=\-?.]).{8,20}$", password):
                return JsonResponse(
                    {"error": "password must include uppercase, lowercase, number, and special character"},
                    status=400
                )

        return self.get_response(request)


             
