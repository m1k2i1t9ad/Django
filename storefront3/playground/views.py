from django.shortcuts import render
from django.core.mail import send_mail, mail_admins, BadHeaderError,EmailMessage
from templated_mail.mail import BaseEmailMessage 
from .tasks import notify_customers
import requests
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
# def say_hello(request):
#     # try:
#     #     #################################
#     #     # #sending emails to site users:
#     #     # send_mail('subject','message',
#     #     #           'info@moshbuy.com', ['bob@moshbuy.com']) #the 3rd argument is the 'from email' and the 4th one is the recipient email list
#     #     #################################
#     #     # # sending emails to site admins:
#     #     # mail_admins('subject','message',html_message='message',)
#     #     ###################################3
#     #     #attaching files with emails:
#     #     message=EmailMessage('subject','message','from@moshbuy.com',['john@moshby.com'])
#     #     message.attach_file('playground/static/images/KSG.jpg')
#     #     message.send()
#     #     ###################################
#     #     #sending templated emails:
#     #     message=BaseEmailMessage(
#     #         template_name='emails/hello.html',
#     #         context={'name':"mosh"}
#     #     )
#     #     message.send(['john@moshbuy.com']) #here the send method differs from the others cuz it requires to insert a recipent email
#     # except BadHeaderError:
#     #     pass
    
    
#     notify_customers.delay('hello')
#     return render(request, 'hello.html', {'name': 'Mosh'})


######################################33
#section7:using the low level cache api:
'''
@cache_page(5*60)
def say_hello(request):
    key='httpbin_result'
    if cache.get(key)is None:
        response=requests.get('https://httpbin.org/delay/2')
        data=response.json()
        cache.set(key,data)
    return render(request, 'hello.html',{'name':cache.get(key)})
'''
######################################33
#caching views:
'''
#instead of using the low level cache api which is tedius, we will use the cache decorator:
@cache_page(5*60) #here we set the timer to 5 minutes
def say_hello(request):
    response=requests.get('https://httpbin.org/delay/2')
    data=response.json()
    return render(request, 'hello.html',{'name':data})
'''
#now waht if we used a class-based view? the @cache_page decorator won't work so we'll need another decorator:
class Helloview(APIView):
    @method_decorator(cache_page(5*60))
    def get(self,request):
        response=requests.get('https://httpbin.org/delay/2')
        data=response.json()
        return render(request, 'hello.html',{'name':'mosh'})
