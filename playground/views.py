from django.shortcuts import render
# from django.core.mail import send_mail, mail_admins, EmailMessage, BadHeaderError
from django.shortcuts import render
from .tasks import notify_customers
# from templated_mail.mail import BaseEmailMessage
def say_hello(request):
    # try:
        #send_mail('suject','message', 'allam@gmail.com', ['mostafaallam602@gmail.com'])

        #mail_admins('subject', 'message', html_message='message') # sending mail to the admin users that defines in the ADMINS settings

        #  message = EmailMessage('sbject', 'message', 'admin@gmail.com',['allam@gmail.com',])
        #  message.attach_file('playground/static/images/mountain.jpg')
        #  message.send()

    #     message = BaseEmailMessage(
    #         template_name='emails/hello.html',
    #         context={'name':'Mostafa'}
    #     )
    #     message.send(to=['allam@email.com'])
    # except BadHeaderError:
    #     pass
    notify_customers.delay('Hello')
    return render(request, 'hello.html', {'name':'Mostafa'})


