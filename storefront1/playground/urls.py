from django.urls import path
from . import views

#URLConf:
urlpatterns=[
    path('hello/',views.say_hello) #no need to add playground/ before hello because we added it once in the main URLConf module(i.e urls.py in storefront)
]