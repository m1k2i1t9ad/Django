from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

#note:
# a view function is a function that takes a reuest and returns a response
#meaning its a request handler
#in some frameworks , it's called action but in django it's called a view

def calculate():
    x=1
    y=2
    return x


def say_hello(request):
    x=calculate()
    # return HttpResponse('Hello World') #comment out the below code if you want to try this one
    return render(request, 'hello.html',{'name':'Mosh'})
