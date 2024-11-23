from django.contrib import admin,messages
from . import models 
from django.db.models.aggregates import Count
#for the "providing links to other pages" topic :
from django.utils.html import format_html ,urlencode
from django.urls import reverse
from django.db.models import QuerySet
from django.contrib import messages
# Register your models here.:
######################################################
#Registering models:
# @admin.register(models.Product) #better way of registering the product than "admin.site.register(models.Product)"
# class ProductAdmin(admin.ModelAdmin):
#     list_display=['title','unit_price'] #displaying only the title and the unit price of the products table
#     list_editable=['unit_price'] # making only the unit_price editable on the admin site
#     list_per_page=10 #listing only 10 products per page
#     #to see the complete listof options, then google  "django modeladmin"

@admin.register(models.Customer)   #better than "admin.site.register(models.Customer)"
class CustomerAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','membership']
    list_editable=['membership']
#############################################################
#Adding a search to the list page:
#for example if we wanted to search the first_name and the last_name of the customer:
    search_fields=['first_name__istartswith','last_name__istartswith'] # the startswith lookup is for sorting and the 'i' is to make  case-insensitive


#
class InventoryFilter(admin.SimpleListFilter):
    title='inventory'
    parameter_name='inventory'
    
    #now we need to use 2 methods for this(the lookups and the queryset):
    def lookups (self,request,model_admin):
        return [
            ('<10', 'Low') #mean if the inventory is < 10, then call it low
        ]
    def queryset(self, request, queryset:QuerySet):
        if self.value()=='<10':
            return queryset.filter(inventory__lt=10)
            
#############################################################33
#Adding Computed Columns:
@admin.register(models.Product)

class ProductAdmin(admin.ModelAdmin):
    list_display=['title','unit_price','inventory_status']
    list_editable=['unit_price']
    list_per_page=10
    search_fields = ['title', 'description']
    
    @admin.display(ordering='inventory') #choosing the inventory field to sort the data in this column
    def inventory_status(self,product): # a function that checks if the inventory status is low or ok
        if product.inventory < 10:
            return 'Low'
        return 'OK'
#############################################################
#adding Filtering to the list page:
#example if want to filter our product by their collection and last update:
    list_filter=['collection','last_update']
#we can also add our own customized filter:
#example if we wanted to add a filter to see only products with low inventory:
    list_filter=['collection','last_update', InventoryFilter] #the inventoryFilter class is created above the productadmin class
    
#############################################################
#Creating custom Actions:
#let say we wanna define a custom action for clearing the inventory for a bunch of products in one go(meaning we wanna set their inventory to zero): 
    actions=['clear_inventory']
    @admin.action(description='Clear inventory')
    def clear_inventory(self,request, queryset): #the 'request' parameter represent the HTTP request and the 'queryset' parameter represent the object that the user has selected
        updated_count=queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were succesfully updated.',
            # messages.ERROR #if we wanted to display an error message instead
        )
#############################################################
#Customizing forms:
#let say we wanted to customize the "add product" form:
    # fields=['title','slug'] #displayin only the title and the slug on the form
    # exclude=['promotions'] #excluding the promotions filed from the form
    # readonly_fields=['title'] #bythis,we can only read the title field (we can't write and submit on it )
    prepopulated_fields={
        'slug':['title'] #prepopulating the slug field based on the title field meaning when we type onthe title, the slug will be automatically populated(typed) too
    }
    autocomplete_fields=['collection'] #to find out more options , google "django model admin" and then on the page click the "model admin options"
#############################################################
#Selecting related objects:
    list_display=['title','unit_price','inventory_status','collection_title']
    list_select_related=['collection']
    
    def collection_title(self,product):
        return product.collection.title
    
#excersice:set up the order page where we can see our orders and their customers(it is done i.e check out the first line on the orderAdmin class)

##############################################################################
#editing Childrren Using inliners:

#so currently, we can create a new order but there is no way to manage the item to an order
#if we want to manage them on the addorder page,then:

class OrderItemLine(admin.TabularInline): #use the "admin.StackedInline" to represent each item as a separate form
    model=models.OrderItem
    autocomplete_fields=['product']
    extra=0 #this removes the default displayed placeholders(comment the code to see the default output or change the number to see the difference)
    #also we can set the min and maxnumber of items for our order:
    min_num=1
    max_num=10
    
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields=['customer'] #customizing the customer field in the add order page
    list_display=['id','placed_at','customer']
    inlines=[OrderItemLine]
    

#############################################################
#overriding the base queryset:
#Sometimes we need to override the base queryset used for rendering list pages.
#example,here on the list of collections,let say we wanna adda new column to show the number of products on each collection:
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display=['title','products_count']
    search_fields=['title'] #search the collections by thier title(this line of code is for the 'customizing forms' topic(section) )
    @admin.display(ordering='products_count')

    # def products_count(self, collection):
    #     return collection.products_count
    
    # #every ModelAdmin has a get_queryset method to overwrite the queryset:
    # def get_queryset(self, request):
    #     return super().get_queryset(request).annotate(
    #         products_count=Count('product')
    #     )
    
#############################################################
#providing links to other pages:
#example, if we want to link the product_count to google.com:
    # def products_count(self, collection):
    #     return format_html('<a href="http://google.com">{}</a>', collection.products_count)
#but if we wanted to link each product_count to its specific collection id: 
    def products_count(self, collection):
        url=(
            reverse('admin:store_product_changelist')  #the general format(formula or syntax) of reverse here is "reverse('admin:app_model_page)"
            + '?'
            + urlencode({
                'collection__id':str(collection.id) #we wrapped it with string function(i.e str) cuz colelction.id returns a number
            })
        )
        return format_html('<a href="{}"> {}</a>', url, collection.products_count)
    #every ModelAdmin has a get_queryset method to overrite the queryset:
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )
        
