from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Solicitud
from .utils import user_directory_path


@receiver(post_save, sender=Solicitud)
def save_document_path(sender, instance, created, **kwargs):
    if created and instance.documentos:
        instance.documentos.name = user_directory_path(instance, instance.documentos.name)
        instance.save(update_fields=['documentos'])
