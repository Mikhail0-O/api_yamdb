from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import CustomUser, Role


@receiver(post_save, sender=CustomUser)
def set_default_role(sender, instance, created, **kwargs):
    if created and not instance.role:
        default_role = Role.objects.get(title='user')
        instance.role = default_role
        instance.save()
