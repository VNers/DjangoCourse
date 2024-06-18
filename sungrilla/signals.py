from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from .models import ActionLog, User


@receiver(pre_save, sender=ActionLog)
def pre_save_handler(sender, instance, **kwargs):
    if instance.user is None:
        anonymous_user, _ = User.objects.get_or_create(username='AnonymousUser')
        instance.user = anonymous_user


@receiver(pre_delete, sender=ActionLog)
def pre_delete_handler(sender, instance, **kwargs):
    instance.save_log_entry()