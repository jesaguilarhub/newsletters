from newsletters.celery import app
from django.core.mail import send_mail

@app.task(name='send_email')
def send_email():
    send_mail(
        subject='Nueva notificación',
        message=f'Esta es una nueva notificación',
        from_email='hola@newsletters.com',
        recipient_list=[],
        html_message=f'<h1>Una nueva notificación</h1>'
    )