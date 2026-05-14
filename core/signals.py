# core/signals.py
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import Repairs, Instruments


@receiver(pre_delete, sender=Repairs)
def update_status_on_repair_delete(sender, instance, **kwargs):
    """При удалении ремонта проверяем, нет ли других активных ремонтов"""
    if instance.instrument and instance.date_of_receipt_from_repair is None:
        # Если удаляем активный ремонт, проверяем другие активные ремонты
        other_active = Repairs.objects.filter(
            instrument=instance.instrument,
            date_of_receipt_from_repair__isnull=True
        ).exclude(pk=instance.pk).exists()

        if not other_active:
            instance.instrument.status = Instruments.STATUS_IN_USE
            instance.instrument.save(update_fields=['status'])