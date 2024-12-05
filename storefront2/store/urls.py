from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
# from pprint import pprint

#URLConf:

'''
urlpatterns=[
    path('products/',views.product_list), 
    path('products/<int:id>/',views.product_detail), #the 'int:' will assign the id to be an integer only (i.e if you typed a letter or non-integer value, the page will display "page not found")
    path('collections/',views.collection_list),
    path('collections/<int:pk>/', views.collection_detail,  name='collection-detail')
]
'''#it's commented since we are not using the function based views anymore
'''
urlpatterns = [
    path('products/', views.ProductList.as_view()),
    path('products/<int:pk>/',views.ProductDetail.as_view()), #the 'int:' will assign the id (or pk) to be an integer only (i.e if you typed a letter or non-integer value, the page will display "page not found")
    path('collections/',views.CollectionList.as_view()),
    path('collections/<int:pk>/', views.CollectionDetail.as_view(),  name='collection-detail')
]
'''

#############################
#routers:
'''
#if we used viewsets,then we need to use routers:
router=DefaultRouter()
router.register('products',views.ProductViewset) #here we're saying that the products endpoint should be manages by the producviewset 
router.register('collection', views.CollectionViewSet)
# pprint(router.urls)

#URLConf
urlpatterns = router.urls
#you can also include other routers like this:
# urlpatterns = [
#     path('',include(router.urls))
# ]
'''
#######################3
#nested routers: allow you to create a hierarchy of routes, which is useful when you have related resources
#got to https://github.com/alanjds/drf-nested-routers to learn more
router=routers.DefaultRouter()
router.register('products',views.ProductViewset,basename='products') #here we're saying that the products endpoint should be manages by the producviewset 
router.register('collections', views.CollectionViewSet)
router.register('carts',views.CartViewSet)
router.register('customers',views.CustomerViewSet)
router.register('orders',views.OrderViewset)
products_router=routers.NestedDefaultRouter(router,'products',lookup='product')
#now on this router, we gonna register a child resource i.e reviews:
products_router.register('reviews',views.ReviewViewSet,basename='product-reviews')#the reason we explicitly set the basename by ourselves is that  by default, django use the queryset attribute to figureout the basename but since we deleted this attribute and now we have a method(on the prodyctviewset),DRF can't figureout what the basename should be called based on the method's logic cuz it's too complex for it


# Set up the nested router for cart items
carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-items')

#URLConf
#now since we have2 routers we can combine their urls and include them in the urlpattenrs objects:


urlpatterns = router.urls+products_router.urls+carts_router.urls