from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User

@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        # Здесь можно добавить логику после создания пользователя
        # Например, отправку кода подтверждения по email/SMS
        print(f"Создан пользователь: {instance.email}")