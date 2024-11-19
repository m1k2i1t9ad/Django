from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q #Q is short for query and using this class we can represent a query expression(a piece of code that produces a value) 
from django.db.models import F #the F class is used to reference a particular field   
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, OrderItem
# Create your views here.

#note:
# a view function is a function that takes a request and returns a response
#meaning its a request handler
#in some frameworks , it's called action but in django it's called a view


def say_hello(request):
    
    '''
    ###################################
    #managers and querysets:
    query_set=Product.objects.all() #the all method is used to pull up all the objects inthe products table
    #query_set=Product.objects.get() #the get method is used to pull up a single object inthe products table
    #query_set=Product.objeccts.filter()#for filtering objects
    for product in query_set:
        print(product)
    '''
    ####################################### 
    #retrieving objects:
    # try:
    #     product=Product.objects.get(pk=0) #we used the try catch cuz pk=0 will get us an error(cuz it's an exception)
    # except ObjectDoesNotExist:
    #     pass
        #another but better way is:
    # product=Product.objects.filter(pk=0).first() #the filter method returns a queryset then "first()" will return the first queryset here in our case since pk=0,it will return none
    # exists=Product.objects.filter(pk=0).exists() #this one returns a boolean value
    
    #########################################
    #filtering objects:
    # queryset=Product.objects.filter(unit_price>20)#this is not correct cuz the expression inside the filter method returns a boolean
    #so inside the filter method, the format must be "keyword=value" like this one:
    # queryset=Product.objects.filter(unit_price__range=(20,30)) #the __range is a special keyword argument(a lookup type). here we are asking a query set with a unitprice ranging from 20 to 30 dollar
    # queryset=Product.objects.filter(title__icontains='coffee')#here the __contains lookup type displayes a title that has the string 'coffee' and the 'i' before is put to make the result case insensetive
    # queryset=Product.objects.filter(last_update__year=2021) #__year is another lookup that here inthis case  diplayes the products with the last_update attribute of 2021
        #so if u want to see more lookups, type "queryset api" on google and click on the first result
    
    ##############################################
    #complex lookups using Q objects:
        #if we want products with inventory<10 AND price<20:
    # queryset=Product.objects.filter(inventory__lt=10, unit_price__lt=20)
        # or:
    # queryset=Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20)
    #or using Q:
    # queryset=Product.objects.filter(
      #  Q(inventory__lt=10) & Q(unit_price__lt=20)) #here the Q class encapsulates the two keyword arguments and became a Q object then we can use bitwise operators (AND,OR...)  
    
    ###################################################
    #referencing fields using F objects:
        #Products: inventory= price (comparing two fields)
    # queryset=Product.objects.filter(inventory=F('unit_price'))
        #using F objects, we can also reference a field in a related table:
    #queryset=Product.objects.filter(inventory=F('collection__id'))
    
    ###########################################################
    #sorting data:
    # queryset=Product.objects.order_by('title') #the products will be sorted in ascending order of their title.put the "-" for descending order i.e "-title"
    # queryset=Product.objects.order_by('unit_price','-title')#now products will be sorted in ascending order of unit_price and descending order of their title
    # queryset=Product.objects.order_by('unit_price','-title').reverse()#now products will be sorted in descending order of unit_price and ascending order of their title
        #combining the filter and order_by metohd:
    # queryset=Product.objects.filter(collection__id=1).order_by('unit_price')
    
    # product=Product.objects.order_by('unit_price')[0] #here eventhough order_by returns a queryset, we won' get that cuz we're requesting the first product element so we'll get an object
        #another way of writing it:
    # product=Product.objects.earliest('unit_price')  #here no need of requesting a queryset then the object, just straight the object(i.e the first product)
        #also there is the latest method:
    # product=Product.objects.latest('unit_price') #returns the latest product element
    
    #############################################################33
    #limiting results:
        #0,1,2,3,4:
    #queryset=Product.objects.all()[:5]
        #5,6,7,8,9:
    #queryset=Product.objects.all()[5:10]
    
    ########################################################
    #selecting fields to query:
    #note: in the template html,remove title from "product.title" to see the correct results for this topic only
    # queryset=Product.objects.values('id','title') #we want to display only the id and title column from our product table in a dicionary form
    # queryset=Product.objects.values_list('id','title','collection__title') #we want to display only the id ,title column, and the title of the collection from our product table in a tuple form
    queryset=Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title') #the distinct method removes the  duplicates
    
    
    ####################################################
    #deferring fields:
    # queryset=Product.objects.only('id','title') #the only method retrieves an instance of the product class(while the values method retreives dictionary objects)
    queryset=Product.objects.defer('description') #the defer method deferes the loading of certain fields to later
    
    
    
    
    return render(request, 'hello.html',{'name':'Mosh','products':list(queryset)}) #here we set the queryset of products in a list and assigned it to a new variable called products(cuz the name is more convenient) then go to the hello.html to make it displayed
    
    
    # return HttpResponse('Hello World') #comment out the below code if you want to try this one
    # return render(request, 'hello.html',{'name':'Mosh'})
    

    