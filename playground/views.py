from django.http import HttpResponse
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product
# Create your views here.

#note:
# a view function is a function that takes a request and returns a response
#meaning its a request handler
#in some frameworks , it's called action but in django it's called a view


def say_hello(request):
    
    '''
    #managers and querysets:
    query_set=Product.objects.all()
    for product in query_set:
        print(product)
    ''' 
    #retrieving objects:
    # try:
    #     product=Product.objects.get(pk=0) #we used the try catch cuz pk=0 will get us an error
    # except ObjectDoesNotExist:
    #     pass
    #another way is:
    product=Product.objects.filter(pk=0).first()
    
    # return HttpResponse('Hello World') #comment out the below code if you want to try this one
    return render(request, 'hello.html',{'name':'Mosh'})
    

    