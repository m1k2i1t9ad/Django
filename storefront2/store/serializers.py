from rest_framework import serializers
from store.models import Product,Collection,Review,Cart,CartItem,Customer,Order,OrderItem
from decimal import Decimal
from django.db.models.aggregates import Count


'''
#creating serializers:
class CollectionSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    title=serializers.CharField(max_length=255)
    
class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title=serializers.CharField(max_length=255)
    # unit_price=serializers.DecimalField(max_digits=6,decimal_places=2)
    #or if we want to renamethe unit_price differently:
    price=serializers.DecimalField(max_digits=6,decimal_places=2,source='unit_price') #the 3rd argument tells djnago to look this value(price) at the unit_price field inthe Product class
    
 ####################################################################
#creating custom serializer fields:   
    price_with_tax=serializers.SerializerMethodField(method_name='calculate_tax')
    def calculate_tax(self,product: Product):
        # Calculate the price with tax:
        return product.unit_price* Decimal(1.1) # here we inserted 1.1 inside the decimalfeild cuz it was a float by default and unit_price i a decimal
 ####################################################################
#serializing realtionships:there are 4 ways to to that:
    #1)primary key:
    collection=serializers.PrimaryKeyRelatedField(   #with this method we can include a primary key or the id of each collection in a product object
        queryset=Collection.objects.all()
    )
    #2)string:
    #if we want the name of each collection:
    collection=serializers.StringRelatedField() #now with this method, django will convert each collection to a string object and return it here
    
    #3)nested object:
    #if we want to include a collection object:
    collection=CollectionSerializer()
    
    #4)Hyperlink:
    #instead of including an object, we can include a hyper link to an end point for viewing that collection:
    collection=serializers.HyperlinkedRelatedField(
        queryset=Collection.objects.all(),
        view_name='collection-detail' #this argument will create the hyperlink
    )
'''
##################################################################
#model serializers:
'''all these fields that are on the above commented code are
also found on the models.py. so there're 2 places where we're 
defining these fields and their validation rules.so if tomorrow
we wanted to change the validation rules(e.g,the title of the
products),there're 2 places where we need to change that rule
(1.in the serializer and 2. in the product class).so the
better way is to use Model Serializers. using the model 
serializer class, we can quickly create a serializer without all those duplications.
'''
#so here is how we can use the model serializer class:
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Collection
        fields=['id','title','products_count']
    products_count=serializers.IntegerField(read_only=True) #the read_only argument is to make the product_counts a non required field(only read)
    # products_count=serializers.SerializerMethodField(method_name='count_products') 
    # def count_products(self, collection: Collection):
    #     return 

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','title','description','slug','inventory','unit_price','price_with_tax','collection']
    # collection=CollectionSerializer() #optional just uncomment it if u want to see the collection object
    price_with_tax=serializers.SerializerMethodField(
        method_name='calculate_tax')
    def calculate_tax(self,product: Product):
        # Calculate the price with tax:
        return product.unit_price* Decimal(1.1) # here we inserted 1.1 inside the decimalfeild cuz it was a float by default and unit_price i a decimal
    
    
    
    #these are the methods that get automatically called behind the scenes when creating a serializer
    # def create(self,validated_data): #create is one of the methods that exists in a base model serialzer class and its called by the save method if you try to create a new product
    #     product=Product(**validated_data)  #unpacking the validated_data dictionary
    #     product.other=1
    #     product.save()
    #     return product
    # def update(self,instance,validated_data):
    #     instance.unit_price=validated_data.get('unit_price')
    #     instance.save()
    #     return instance
    
    
    #a serializer class for building the reviews API:
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields=['id','date','name','description']
            
    def create(self,validated_data):
        product_id=self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)
    
    
    
    
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','title','unit_price']
    
class CartItemSerializer(serializers.ModelSerializer):
    id=serializers.UUIDField(read_only=True)
    product = SimpleProductSerializer() #we used this  serializer instead of ProductSerilaizer cuz we only wanted some of fileds of the product to be displayed(not all of them) 
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id','product', 'quantity','total_price']

    def get_total_price(self, cart_item:CartItem):
        return cart_item.quantity *cart_item.product.unit_price
    

class CartSerializer(serializers.ModelSerializer):
    id=serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)  # Use 'items' for related name
    total_price=serializers.SerializerMethodField(
        method_name='calculate_total_price')
    class Meta:
        model=Cart
        fields=['id','items','total_price']
       
    def calculate_total_price(self, cart: Cart):
        # total = 0 #It initializes a total variable to accumulate the total price.
        # for item in cart.items.all():  # Assuming a related name for cart items
        #     product = item.product  # Access the product from the cart item
        #     total += product.unit_price * item.quantity  # Calculate total price
        # return total
        #or simply:
        return sum([item.quantity*item.product.unit_price for item in cart.items.all()])
       
class AddCartItemSerializer(serializers.ModelSerializer):
    product_id=serializers.IntegerField()
    #here for this serializer, we can't rely on the default save method.instead we will overwrite it to based onthe requirement of our app:
    
    def validate_product_id(self,value):
        if not Product.objects.filter(pk=value).exists():
            raise  serializers.ValidationError('No product with the given id has found')
        return value         
    def save(self,**kwargs):
        cart_id=self.context['cart_id']
        product_id=self.validated_data['product_id']
        quantity=self.validated_data['quantity']
        
        try:
            cart_item=CartItem.objects.get(cart_id=cart_id,product_id=product_id)
            cart_item.quantity +=quantity
            cart_item.save()
            self.instance=cart_item
        except CartItem.DoesNotExist:
            self.instance=CartItem.objects.create(cart_id=cart_id, **self.validated_data)
            
        return self.instance
    class Meta:
        model=CartItem
        fields=['id','product_id','quantity']
        
        
class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields=['quantity']
         
         
#a serializer class for  building the Profile API:
class CustomerSerializer(serializers.ModelSerializer):
    user_id=serializers.IntegerField(read_only=True)
  
    
    class Meta:
        model=Customer
        fields=['id','user_id','phone','birth_date','membership']
        
        
        
class OrderItemSerializer(serializers.ModelSerializer):
    id=serializers.UUIDField(read_only=True)      
    product = SimpleProductSerializer() #we used this  serializer instead of ProductSerilaizer cuz we only wanted some of fileds of the product to be displayed(not all of them) 
    class Meta:
        model = CartItem
        fields = ['id','product', 'quantity','total_price']

        
class OrderSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)  # Use 'items' for related name
    class Meta:
        model=Order
        fields=['id','customer','placed_at','payment_status','items']