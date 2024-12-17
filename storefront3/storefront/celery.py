import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE','storefront.settings')

celery=Celery('storefront') #creting a celery instance and naming it 'storefront'
#then specify where celery can find the configuration varialbles:
celery.config_from_object('django.conf:settings',namespace='CELERY') #the 2nd argument says that all our configuration settings should start with 'CELERY'

celery.autodiscover_tasks() #by calling this method we're asking celery to automatically discover all these 
#now go to __init__.py on the storefront and import celery there inorder for python to see this code