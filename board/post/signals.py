from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Response

@receiver(post_save, sender=Response)
def notify_about_response(sender, instance, created, **kwargs):
    if created:
        # Уведомление автору объявления о новом отклике
        subject = f'Новый отклик на ваше объявление "{instance.post.title}"'
        message = render_to_string('emails/new_response_notification.html', {
            'response': instance,
            'post': instance.post,
        })
        send_mail(
            subject=subject,
            message='',
            html_message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.post.author.email],
            fail_silently=False,
        )
    elif instance.status == Response.Status.ACCEPTED:
        # Уведомление автору отклика о принятии
        subject = f'Ваш отклик на объявление "{instance.post.title}" принят'
        message = render_to_string('emails/response_accepted_notification.html', {
            'response': instance,
            'post': instance.post,
        })
        send_mail(
            subject=subject,
            message='',
            html_message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.author.email],
            fail_silently=False,
        )