#tasks.py is one of the modules that we instructed celery to automatically discover
from time import sleep #used for simulating a long running task
from celery import shared_task

@shared_task
def notify_customers(message):
    print('sending 10k emails....')
    print(message)
    sleep(10) #sleep for 10 seconds
    print('Emails were successfully sent!')