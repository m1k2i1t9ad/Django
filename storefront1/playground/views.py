from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q #Q is short for query and using this class we can represent a query expression(a piece of code that produces a value) 
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, OrderItem, Order, Customer
from django.db.models.aggregates import Count, Max,Min,Avg,Sum
from django.db.models import Value,F ,Func , ExpressionWrapper ,DecimalField
#the F class is used to reference a particular field   
from django.db.models.functions import Concat
from django.contrib.contenttypes.models import ContentType
from store.models import Product, Collection
from tags.models import TaggedItem
from django.db import transaction ,connection

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
    #    Q(inventory__lt=10) & Q(unit_price__lt=20)) #here the Q class encapsulates the two keyword arguments and became a Q object then we can use bitwise operators (AND,OR...)  
    
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
    # queryset=Product.objects.all()[5:10]
    
    ########################################################
    #selecting fields to query:
    #note: in the template html,remove title from "product.title" to see the correct results for this topic only
    # queryset=Product.objects.values('id','title') #we want to display only the id and title column from our product table in a dicionary form
    # queryset=Product.objects.values_list('id','title','collection__title') #we want to display only the id ,title column, and the title of the collection from our product table in a tuple form
    # queryset=Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title') #the distinct method removes the  duplicates
    
    
    ####################################################
    #deferring fields:
    # queryset=Product.objects.only('id','title') #the only method retrieves an instance of the product class(while the values method retreives dictionary objects)
    # queryset=Product.objects.defer('description') #the defer method deferes the loading of certain fields to later
    
    #######################################################
    #selecting related objects:
    #we use the select_related method when the other end of relationship instance is only 1
    # queryset=Product.objects.select_related('collection').all() #here a product has only one collection
    #we use prefetch_related when the other end of the relationship has many objects
    # queryset=Product.objects.prefetch_related('Promotions').select_related().all()#here one product has many promotions
    
    #excercise:
    # queryset=Order.objects.select_related('customer').order_by('-placed_at')[:5]
    # return render(request, 'hello.html',{'name':'Mosh','orders':list(queryset)}) #here we set the queryset of orders in a list and assigned it to a new variable called orders(cuz the name is more convenient) then go to the hello.html to make it displayed
    
    ##################################################################
    # #Aggregating Objects:
    # result=Product.objects.aggregate(count=Count('id'),min_price=Min('unit_price'))
    # return render(request, 'hello.html',{'name':'Mosh','result':result })
    #######################################################################
    #Annotating objects:
    #we can't pass a boolean value for annotation only expressions
    # queryset=Customer.objects.annotate(is_new=True)#this will result an error
    # queryset=Customer.objects.annotate(is_new=Value(True))#this will work and in the query you can see he is_new values
    # queryset=Customer.objects.annotate(new_id=F('id'))
    # return render(request, 'hello.html',{'name':'Niggalacious','result':list(queryset) })
    ###############################################################
    #calling database functions:
    '''
    queryset=Customer.objects.annotate(
        #CONCAT:for concatinating strings
        full_name=Func(F('first_name'), Value(' '), F('last_name'),function='CONCAT')
    )
    #or we can import the concat function and do this:
    queryset=Customer.objects.annotate(
        #CONCAT
        full_name=Concat('first_name', Value(' '), 'last_name')
    )
    return render(request, 'hello.html',{'name':'Niggalacious','result':list(queryset) })
    '''
    #################################################################################3
    #Grouping Data:
    ''' 
    queryset=Customer.objects.annotate(
        orders_count=Count('order')
    )
    return render(request, 'hello.html',{'name':'Niggalacious','result':list(queryset) })
    '''
    ####################################################################
    #Working with Expression Wrappers:
    '''
    discounted_price=ExpressionWrapper(F('unit_price')* 0.8 , output_field=DecimalField() )
    queryset=Product.objects.annotate(discounted_price =discounted_price )
    
    return render(request, 'hello.html',{'name':'Niggalacious','result':list(queryset) })
    '''
    ###########################################################################################
    #Querying Generic Relationships:
    '''
    #for a example if we want to get the tags for a given product:
    content_type=ContentType.objects.get_for_model(Product)
    queryset=TaggedItem.objects \
    .select_related('tag') \
    .filter(
        content_type=content_type,
        object_id=1
    )
    #or simply create a taggeditemmanager class in tags.py then:
    TaggedItem.objects.get_tags_for(Product, 1) #checkout the TaggedItemManager function to understand this
    return render(request, 'hello.html',{'name':'Niggalacious','tags':list(queryset) })
    
    #note:the "\" was used to tell the editor that the lines are in continuation( in chain)
    
    '''
    ########################################################################
    #understanding queryset Cache:
    '''
    queryset=Product.objects.all()
    list(queryset)#this will make it get stored in a queryset cache
    list(queryset)#this will just read the result from the queryset cache

    return render(request, 'hello.html',{'name':'Mosh'})
    '''
    #############################################################################
    #creating objects:
    '''
    collection=Collection()
    collection.title='Video Games'
    collection.featured_product=Product(pk=1)
    collection.save()
    
    
    #or shortly(not recommended):
    # collection=Collection.objects.create(name='a',featured_product_id=1)#but this method has problems 
    # collection.id
    
    return render(request, 'hello.html',{'name':'Mosh'})#go and check the sql query to uderstand everything (about the above codes)
    '''
    ########################################################################################
    #Updating Objects:
    '''
    # collection=Collection(pk=11)
    # collection.title='Games' #here if we didn't write this, djnago will update the title to an emplty string by default
    # collection.featured_product=None
    # collection.save()
    
    #so shortly(recommended):
    Collection.objects.filter(pk=11).update(featured_product=None) #this one is better and doesn't have the above issue (about the title)
    
    return render(request, 'hello.html',{'name':'Mosh'})
    '''
    ###################################################################################
    #deleting objects:
    '''
    collection=Collection(pk=11)
    collection.delete()#this will delete the specified collection as above
    #to delete multiple colections:
    Collection.objects.filter(id_gt=5).delete()
    return render(request, 'hello.html',{'name':'Mosh'})
    '''
    ####################################################################3#########
    #Traansactions:
    '''
    with transaction.atomic():
        order=Order()
        order.customer_id=1
        order.save()
        
        item=OrderItem()
        item.order=order
        item.product_id=1
        item.quantity=1
        item.unit_price=10
        item.save()
    return render(request, 'hello.html',{'name':'Mosh'})
    '''
    #some notes:    
    '''
     In the context of database transactions, the with statement is used to define a block of code where all database operations are treated as a single unit of work
     transaction.atomic(): This is a context manager provided by Django's transaction module that ensures atomicity.
     atomic(): This function guarantees that all database operations within the block are either committed together or rolled back if any operation fails, maintaining data integrity.
    '''
    #################################################################
    #executing raw SQL Queries:
    queryset=Product.objects.raw('SELECT id,title FROM store_product')# this will return a 'raw' queryset
    #or;
    with connection.cursor() as cursor:
        cursor.execute('SELECT id,title FROM store_product')
        
    
    #django aculally do all this for us but you can use this approach when:
        #dealing with complex queries(annotations,filters...)
        #the query that django generates doesn't perform well
        
    return render(request, 'hello.html',{'name':'Mosh', 'result':list(queryset)})
    
    
    
    
    
    # return render(request, 'hello.html',{'name':'Mosh','products':list(queryset)}) #here we set the queryset of products in a list and assigned it to a new variable called products(cuz the name is more convenient) then go to the hello.html to make it displayed
    #note comment out the above return statement fot the topics that include product
    
    # return HttpResponse('Hello World') #comment out the below code if you want to try this one
    # return render(request, 'hello.html',{'name':'Mosh'})
    

    