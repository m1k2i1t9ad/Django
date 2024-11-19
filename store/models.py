from django.db import models


# Create your models here.


class Promotion(models.Model):
    description=models.CharField(max_length=255)
    discount=models.FloatField()

class Collection(models.Model):
    title=models.CharField(max_length=255)
    featured_product=models.ForeignKey(
        "Product", on_delete=models.SET_NULL, null=True, related_name='+' ) 

class Product(models.Model):
    # sku=models.CharField(max_length=10,primary_key=True) #not needed
    title=models.CharField(max_length=255)
    slug=models.SlugField()
    description=models.TextField()
    unit_price=models.DecimalField(max_digits=6,decimal_places=2) #decimalfield is better that floatfield for monetary values
    inventory=models.IntegerField()
    last_update=models.DateTimeField(auto_now=True)
    collection=models.ForeignKey(Collection,on_delete=models.PROTECT) #the "PROTECT" value means that if you accidentally deleted Collection,we won't end up deleting all products in that Collection
    Promotions=models.ManyToManyField(Promotion)#manytomany relationships meaning product can have many promotions and a promotion can apply to defferent products
    
    
class Customer(models.Model):
    MEMBERSHIP_BRONZE= 'B'
    MEMBERSHIP_SILVER= 'S'
    MEMBERSHIP_GOLD= 'G'

    MEMBERSHIP_CHOICES=[
        (MEMBERSHIP_BRONZE,'Bronze'),
        (MEMBERSHIP_SILVER,'Silver'),
        (MEMBERSHIP_GOLD,'Gold')
    ]
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=15)
    birth_date=models.DateField(null=True)
    membership=models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default='MEMBERSHIP_BRONZE')

    class Meta:
        # Specify metadata options for the model
        db_table = 'store_customer'  # Custom table name in the database
        indexes = [   # Create an index on 'last_name' and 'first_name'
        models.Index(fields=['last_name', 'first_name'])
        # This improves search performance for queries filtering by these fields
        ]
        
        
class Order(models.Model):
    PAYMENT_STATUS_PENDING= 'P'
    PAYMENT_STATUS_COMPLETE= 'C'
    PAYMENT_STATUS_FAILED= 'F'
    
    PAYMENT_STATUS_CHOICES=[
        (PAYMENT_STATUS_PENDING,'Pending'),
        (PAYMENT_STATUS_COMPLETE,'Complete'),
        (PAYMENT_STATUS_FAILED,'Failed')
    ]

    placed_at=models.DateTimeField(auto_now_add=True) #the "auto_now_add=True" means that on the first time we create an order, django automatically populates the DateTimeField
    payment_status=models.CharField(max_length=1,choices=PAYMENT_STATUS_CHOICES,default=PAYMENT_STATUS_PENDING)
    customer=models.ForeignKey(Customer,on_delete=models.PROTECT) #again "PROTECT" means that if you accidentally deleted Customer,you won't end up deleting orders
    # note:in fact, you should never delete orders from from your database 

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.PROTECT, related_name='+') #"PROTECT" means that if you accidentaly delete an order,you don't endup deleting the orderItems
    product=models.ForeignKey(Order,on_delete=models.PROTECT, related_name='+') #"PROTECT" means that if you accidentaly delete a product,you don't endup deleting the orderItems
    quantity=models.PositiveIntegerField()
    unit_price=models.DecimalField(max_digits=6,decimal_places=2)    



class Address(models.Model):
    street=models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    # customer=models.OneToOneField(Customer,on_delete=models.CASCADE,primary_key=True) # the CASCADE value on the on_delete argument means that if we delete the customer, the associated address also will be deleted
    # #note: the primary key on the customers is important because if we don't set it we won't have OneToOne relationship 
    #if we want oneTomany relationship:
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE) # the CASCADE value on the on_delete argument means that if we delete the customer, the associated address also will be deleted
    zip_code=models.CharField(max_length=50 , null=True)
    
    
class Cart(models.Model):
  created_at=models.DateTimeField(auto_now_add=True)
  
class CartItem(models.Model):
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE) # the CASCADE value on the on_delete argument means that if we delete the cart, the associated cartItem also will be deleted
    product=models.ForeignKey(Product, on_delete=models.CASCADE) # the CASCADE value on the on_delete argument means that if we delete the product, the associated cartitem also will be deleted
    quantity=models.PositiveIntegerField()