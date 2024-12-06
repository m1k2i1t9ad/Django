from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from store.models import Customer

#in django, we use signas to decouple our apps and prevent them from stepping on each other toes
#here we will use the post_save signal to create a customer inside the store right after the a user is registered(created) on the core app
@receiver(post_save, sender=settings.AUTH_USER_MODEL) #we didn't use sender=User cuz the user is on the core app which will make the store app dependent on it
def create_customer_for_new_user(sender,**kwargs): #this method here is called a signal handler 
    if kwargs['created']:
        Customer.objects.create(user=kwargs['instance'])
#now you can import this method on the store/apps.py by overwriting the ready method inside the storeconfig class