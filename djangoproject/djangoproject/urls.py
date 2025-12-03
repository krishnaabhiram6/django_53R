"""
URL configuration for djangoproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from basic.views import func
from django.urls import path
from basic.views import sample,sample1,sampleinfo,dynamicResponse,add,health,addStudent,job1,job2,signUp,check,login,change_password,getAllUsers



urlpatterns = [
    path('admin/', admin.site.urls),
    path('fun/',func),
    path('greet/',sample),
    path('53r',sample1),
    path('info',sampleinfo),
    path('dynamic/',dynamicResponse),
    path('add/',add),
    path('health/',health),
    path('student/',addStudent),
    path('job1/',job1),
    path('job2/',job2),
    path('signup/',signUp),
    path('check/',check),
    path('login/',login),
    path('change_password/',change_password),
    path('users/',getAllUsers)
    

]


#get,post,put,delete

