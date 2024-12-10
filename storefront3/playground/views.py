from django.shortcuts import render
from django.core.mail import send_mail, mail_admins, BadHeaderError


def say_hello(request):
    try:
        send_mail('subject','message',
                  'info@moshbuy.com', ['bob@moshbuy.com']) #the 3rd argument is the 'from email' and the 4th one is the recipient email list
    except BadHeaderError:
        pass
    return render(request, 'hello.html', {'name': 'Mosh'})
