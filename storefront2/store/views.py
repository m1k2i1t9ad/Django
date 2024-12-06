from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Collection,Review,Cart,CartItem,Customer,Order,OrderItem
from .serializers import ProductSerializer,CollectionSerializer,ReviewSerializer,CartSerializer,CartItemSerializer,AddCartItemSerializer,UpdateCartItemSerializer,CustomerSerializer,OrderSerializer,OrderItemSerializer,CreateOrderSerializer,UpdateOrderSerializer
from rest_framework import status
from django.db.models.aggregates import Count
from rest_framework.views import APIView #this is the base class for all class based views
from rest_framework.mixins import ListModelMixin,CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView #for generic views
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend #this backend gives us generic filtering
from .filters import ProductFilter
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination #using this class we can paginate data using a page number
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny,DjangoModelPermissions
from .permissions import IsAdminOrReadOnly,FullDjangoModelPermissions,viewCustomerHistoryPermission

# Create your views here.

#serializing objects:
'''
@api_view()
def product_list(request):
    queryset=Product.objects.select_related('collection').all()
    serializer=ProductSerializer(queryset, many=True,context={'request': request}) #the second argument tells the serializer that it should iterate over the queryset and convert each product object to a dictionary
    return Response(serializer.data) # this is better than return HttpResponse('serializer.data')

@api_view()
def product_detail(requset, id):
    product=get_object_or_404(Product,pk=id)#this means if we searched for a product that doesn't exist ,it will display "404 not found" instead of the "doesn't exist" exception
    serializer=ProductSerializer(product) #this serializer will convert our product to a dictionary
    return Response(serializer.data) #this well get us the dictionary that we got above
 
@api_view()   
def collection_detail(request,pk):
    return Response('ok')
'''

##################################################################
#Deseriaizing objects:
''' deserialization happens when you recieve a data from the
client.lets say the client wants to create a new product,to do
this, first, we should send a post request to the products end
point and inthe body of the request,we should include a product
object.now on the server,we haveto read the data inthe data 
inthe body of the request and deserialize it so we get a product
object and store it on the database'''
#lets see how this works:
#1)creating and saving objects:here we'll be able create and save the product:
'''
@api_view(['GET','POST']) #we didn't do this in the previous lesson cuz the Get httpmethod was already set by default but since we need POST here, we passed them inside an array like this
def product_list(request):
    if request.method=='GET':
        queryset=Product.objects.select_related('collection').all()
        serializer=ProductSerializer(
            queryset, many=True,context={'request': request}) #the second argument tells the serializer that it should iterate over the queryset and convert each product object to a dictionary
        return Response(serializer.data) # this is better than return HttpResponse('serializer.data')
    elif request.method=='POST':  #this is where the deseialization happens
        serializer=ProductSerializer(data=request.data) #the ProductSerializer will deserialize the data(i.e request.data)
        #sub topic:data validation:
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # print(serializer.validated_data) #this will validate the data
        return Response(serializer.data,status=status.HTTP_201_CREATED)

#2)updating and deleting objects:here the product detail will be updated when we make some changes and we will abe able to delete it when we need to:
@api_view(['GET','PUT','DELETE'])
def product_detail(request, id):
    product=get_object_or_404(Product,pk=id)#this means if we searched for a product that doesn't exist ,it will display "404 not found" instead of the "doesn't exist" exception
    if request.method=='GET':
        serializer=ProductSerializer(product) #this serializer will convert our product to a dictionary
        return Response(serializer.data) #this well get us the dictionary that we got above
    elif request.method=='PUT':
        serializer=ProductSerializer(product,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method=='DELETE':
        if product.orderitems.count()>0:
            return Response({"error: product can't be deleted cuz it is associated with an item order"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
@api_view(['GET','POST'])
def collection_list(request):
    if request.method=="GET":
        queryset=Collection.objects.annotate(products_count=Count('products')).all()
        serializer=CollectionSerializer(queryset,many=True)
        return Response(serializer.data)
    elif request.method=="POST":
        serializer=CollectionSerializer(data=request.data)
        seriaizer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        

@api_view(['GET','POST','DELETE'])   
def collection_detail(request,pk):
    collection=get_object_or_404(
        Collection.objects.annotate(
            products_count=Count('products')),pk=pk)
    if request.method=='GET':
        serializer=CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method=='PUT':
        serializer=CollectionSerializer(collection,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method=='DELETE':
        if collection.products.count()>0:
            return Response({"error: collection can't be deleted cuz it is associated with an item order"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
 '''   



####################################################################33
#class based views:are better than the function views that are commented above
'''
class ProductList(APIView): #instead of the product_list function
    def get(self,request):
        queryset=Product.objects.select_related('collection').all()
        serializer=ProductSerializer(
            queryset, many=True,context={'request': request}) #the second argument tells the serializer that it should iterate over the queryset and convert each product object to a dictionary
        return Response(serializer.data) # this is better than return HttpResponse('serializer.data')
    def post(self,request):
        serializer=ProductSerializer(data=request.data) #the ProductSerializer will deserialize the data(i.e request.data)
        #sub topic:data validation:
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # print(serializer.validated_data) #this will validate the data
        return Response(serializer.data,status=status.HTTP_201_CREATED)

class ProductDetail(APIView):
    def get(self,request,id):
        product=get_object_or_404(Product,pk=id)
        serializer=ProductSerializer(product) #this serializer will convert our product to a dictionary
        return Response(serializer.data) #this well get us the dictionary that we got above
    def put(self, request,id):
        product=get_object_or_404(Product,pk=id)
        serializer=ProductSerializer(product,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    def delete(self,request,id):
        product=get_object_or_404(Product,pk=id)
        if product.orderitems.count()>0:
            return Response({"error: product can't be deleted cuz it is associated with an item order"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    '''
    
############################################################33
#Generic views:
'''
class ProductList(ListCreateAPIView):
    
    #overwriting the get quseryset and get serializer methods:
    # def get_queryset(self):
    #     return Product.objects.select_related('collection').all()
    # def get_serializer_class(self):
    #     return ProductSerializer #here we're returning the class not an object 
    # def get_serializer_context(self):
    #     return {'request':self.request}
    
    #or more simply:
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    def get_serializer_context(self):
        return {'request':self.request}
    
    
class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    def delete(self,request,pk):
        product=get_object_or_404(Product,pk=pk)
        if product.orderitems.count()>0: #we didn't overwrite the delete method using the destriy apiview cuz of this specific logic here so we will just adjust it like this
            return Response({"error: product can't be deleted cuz it is associated with an item order"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
class CollectionList(ListCreateAPIView):
    queryset=Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class=CollectionSerializer

    
class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset=Collection.objects.annotate(products_count=Count('products'))
    serializer_class=CollectionSerializer
    def delete(self,request,pk):
        collcetion=get_object_or_404(Collection,pk=pk)
        if collection.products.count()>0:
            return Response({"error: collection can't be deleted cuz it is associated with an item order"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
'''
####################################################################
#Viewsets:used to combine a set of related views:
#e.g: of we want to combine the related  views on the productlist and productdetail class:
class ProductViewset(ModelViewSet): #also check out the ReadOnlyModel1ViewSet module 
    # queryset=Product.objects.all()
    ##########################################3
    #subtopic1:filtering:
    
    # #here if we wanted to filter the products by a specific collection:
    # #fisrt comment the above queryset cuz since we can't call the filter method there,we will overwrite the get queryset method:
    # def get_queryset(self):
    #     queryset=Product.objects.all()
    #     collection_id=self.request.query_params.get('collection_id')#the get method returns none if we don't have a key with "collection_id"
    #     if collection_id is not None:
    #         queryset=queryset.filter(collection_id=collection_id)#this will filter the products by a specific collection
    #     return queryset
    
    #############################################
    #subtopic2:Generic filtering:
    # ''''on the above, we implemented  basic filtering but, what if we
    # wanted to filter our products by another field additionally? then
    # the above logic will get more complicated.this is where we use 
    # generic filtering.so we gonna use a third-party library called 
    # "django filter" so we can easily filter any models by any fileds.
    # 1st:on the terminal type: pipenv install django-filter
    # 2nd:on settings.py/INSTALLED_APPS, add 'django_filters'
    # '''
    #3rd:the above code for filtering is commented cuz we don't need it we easily write:
    queryset=Product.objects.all()
    filter_backends=[DjangoFilterBackend]#with this backend all we have to do is specify what fields are we gonna use for filtering:
    # filterset_fields=['collection_id'] 
    #if u want to filter by class, commentout the filterset_fields and:
    filterset_class=ProductFilter  #go to https://django-filter.readthedocs.io/en/stable/ to learn more
    #############################################
    #subtopic3:Searching:if we wanted to search based on let say the title and description of the product:
    filter_backends=[DjangoFilterBackend,SearchFilter]
    search_fields=['title','description']
    ##########################################
    #subtopic4:Sorting:if we wanted to sort our products by lets say their unit_price and last_update :
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    ordering_fields=['unit_price','last_update']
    ##########################################
    #applying custom permisssion:
    permission_classes=[IsAdminOrReadOnly] #this is a subtopic from the authentication section
    ##########################################
    #subtopic5:Pagination:
    pagination_class=PageNumberPagination#after this, go to settnigs.py and set the pagesize on the rest_framework object
    #or simply just on the settings.py, on the rest_framework objects ,set the default(global) pagination class and that's it u won't need the above commented code
    
    
    serializer_class=ProductSerializer #cuz these 2 lines are same in both classes
    
    def get_serializer_context(self):
        return {'request':self.request}
    
    def delete(self,request,pk):
        product=get_object_or_404(Product,pk=pk)
        if product.orderitems.count()>0: #we didn't overwrite the delete method using the destriy apiview cuz of this specific logic here so we will just adjust it like this
            return Response({"error: product can't be deleted cuz it is associated with an order item"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
#by the above implementation,we won't need the ProductList ad ProductDetail class anymore
    

#also we can do the same for the collectionList and collectinDetail class:
class CollectionViewSet(ModelViewSet):
    queryset=Collection.objects.annotate(products_count=Count('products'))
    serializer_class=CollectionSerializer
    def delete(self,request,pk):
        collcetion=get_object_or_404(Collection,pk=pk)
        if collection.products.count()>0:
            return Response({"error: collection can't be deleted cuz it is associated with an item order"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
     ##########################################
    #applying custom permisssion:
    permission_classes=[IsAdminOrReadOnly] #this is a subtopic from the authentication section
    ##########################################
    
class ReviewViewSet(ModelViewSet):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])
    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}
    
    
class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet): #we did this instead of modelviewset cuz we won't need the update and list model mixins for this case
    queryset=Cart.objects.prefetch_related('items__product').all()
    serializer_class=CartSerializer
class CartItemViewSet(ModelViewSet):
    http_method_names=['get','post','patch','delete'] #to prevent the put request(or method) from this viewset
    #here we need to return 2 serializers depending on the requset so we need to overwrite the getserializer method:
    def get_serializer_class(self):
        if self.request.method=='POST':
            return AddCartItemSerializer
        elif self.request.method=='PATCH': #we used PATCH instead of PUT cuz we wan to update a specific part of our cartitem object
            return UpdateCartItemSerializer
        return CartItemSerializer
    #we need also to overwrite the the get_serializer_context method cuz in serializers, we don't have access to url parameters:
    def get_serializer_context(self):
        return {'cart_id':self.kwargs['cart_pk']}
    
    def get_queryset(self):
       return CartItem.objects\
           .filter(cart_id=self.kwargs['cart_pk']) \
           .select_related ('product')
           
           
#a viewset forbuilding the profile API:
class CustomerViewSet(ModelViewSet):
    queryset=Customer.objects.all()
    serializer_class=CustomerSerializer
    
    ############################################
    #applying permissions:
    permission_classes=[IsAdminUser]
    '''
    #let say we want anyone tobe able to retriev a customer object but only authenticated users or admin users can update a customer object:
    def get_permissions(self):
        if self.request.method=='GET':
            return [AllowAny()] #here we allowed unrestricted access to the GET method to any user
        return [IsAuthenticated()] #means methods otherthan GET require authentication
    '''
    ############################################
    '''
    #applying model permissions:
    permission_classes=[DjangoModelPermissions]
    #we can overwrite the djangmodelperissions class for specific purposes inside permissions.py and the import it here then use it like this:
    permission_classes=[FullDjangoModelPermissions]
    '''
    ############################################
    #applying custom model permissions: 
    @action(detail=True,permission_classes=[viewCustomerHistoryPermission])
    def history(self,request,pk): #adding an endpoint with the form store/customers/id/history
        return Response('ok')
    
    ############################################
    #getting current user's profile:
    #note:all these methods that're inside the customerviewset the below method are also called actions
    #adding an endpoint called store/customers/me:
    #in this case we are defining a custom action and we need to decorate it with an action decorator  in rest-framework
    @action(detail=False, methods=['GET','PUT'],permission_classes=[IsAuthenticated]) #setting the detail to false means that the action will be available on the list not on the detail view
    def me(self, request):
        # Retrieve or create the customer profile for the current user
        customer=Customer.objects.get(user_id=request.user.id)
        if request.method=='GET':
            serializer=CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method=='PUT':
            serializer=CustomerSerializer(customer,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        
        
class OrderViewset(ModelViewSet):
    # queryset=Order.objects.all() #if we want all the niggaz to access all the orders
    # serializer_class=OrderSerializer
    # permission_classes=[IsAuthenticated] #if we want all the autheticated users to be able to delete and update the orders 
    #but if we wanted to allow that only to the admin users,we need to overwrite the get_permissions method:
    http_method_names=['get','post','patch','delete','head','options']
    def get_permissions(self):
        if self.request.method in ['PATCH','DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    #returning the created order:to do that we need to overwrite the createmodelmixin:
    def create(self,request, *args,**kwargs):
        serialzer=CreateOrderSerializer(
            data=request.data,
            context={'user_id':self.request.user.id}
        )
        serialzer.is_valid(raise_exception=True)
        order=serialzer.save()
        serialzer=OrderSerializer(order)
        return Response(serialzer.data)
    
    
    def get_serializer_class(self):
        if self.request.method=='POST':
            return CreateOrderSerializer
        elif self.request.method=='PATCH':
            return UpdateOrderSerializer
        return OrderSerializer
    
    #if we wanted to make all the orders available only for the admin users, then we need to overwrite the get queryset method:
    def get_queryset(self):
        user=self.request.user
        if user.is_staff:
            return Order.objects.all()  # Admins can access all orders
        
        customer_id=Customer.objects.only('id').get(user_id=user.id)
        return Order.objects.filter(customer_id=customer_id)
    