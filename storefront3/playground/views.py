from django.shortcuts import render
from django.core.mail import send_mail, mail_admins, BadHeaderError,EmailMessage
from templated_mail.mail import BaseEmailMessage 
from .tasks import notify_customers
def say_hello(request):
    # try:
    #     #################################
    #     # #sending emails to site users:
    #     # send_mail('subject','message',
    #     #           'info@moshbuy.com', ['bob@moshbuy.com']) #the 3rd argument is the 'from email' and the 4th one is the recipient email list
    #     #################################
    #     # # sending emails to site admins:
    #     # mail_admins('subject','message',html_message='message',)
    #     ###################################3
    #     #attaching files with emails:
    #     message=EmailMessage('subject','message','from@moshbuy.com',['john@moshby.com'])
    #     message.attach_file('playground/static/images/KSG.jpg')
    #     message.send()
    #     ###################################
    #     #sending templated emails:
    #     message=BaseEmailMessage(
    #         template_name='emails/hello.html',
    #         context={'name':"mosh"}
    #     )
    #     message.send(['john@moshbuy.com']) #here the send method differs from the others cuz it requires to insert a recipent email
    # except BadHeaderError:
    #     pass
    
    notify_customers.delay('hello')
    return render(request, 'hello.html', {'name': 'Mosh'})
