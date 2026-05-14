from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import CASCADE


class Instruments(models.Model):
    STATUS_IN_USE = "IN_USE"
    STATUS_IN_REPAIR = "IN_REPAIR"
    STATUS_RELOCATED = "RELOCATED"
    STATUS_BROKEN = "BROKEN"

    STATUS_CHOICES = [
        (STATUS_IN_USE, "в работе"),
        (STATUS_IN_REPAIR, "в ремонте"),
        (STATUS_RELOCATED, "перемещен"),
        (STATUS_BROKEN, "сломан"),
    ]
    external_id = models.CharField(max_length=100, null=True, blank=True, unique=True)
    name = models.CharField(max_length=100, verbose_name="Наименование")
    inventory_number = models.IntegerField(
        unique=True,
        null=True,
        blank=True,
        verbose_name="Инвентарный номер",
    )
    entry_date = models.DateField(verbose_name="Дата ввода")
    price = models.DecimalField(decimal_places=2, max_digits=8, verbose_name="Цена")
    is_new = models.BooleanField(default=True) #не используется. Для пометки, что инструмент был приобретён новым
    image1 = models.ImageField(
        upload_to="instruments/foto", verbose_name="Фото инструмента1"
    )
    image2 = models.ImageField(
        upload_to="instruments/foto", verbose_name="Фото инструмента2", blank=True
    )
    image3 = models.ImageField(
        upload_to="instruments/foto", verbose_name="Фото инструмента3", blank=True
    )
    comment = models.TextField(max_length=200, verbose_name="Комментарий")
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default=STATUS_IN_USE
    )

    @property
    def status_badge(self):
        return {
            "IN_USE": ("В работе", "success"),
            "IN_REPAIR": ("В ремонте", "warning"),
            "BROKEN": ("Сломан", "danger"),
            "RELOCATED": ("Перемещен", "secondary"),
        }.get(self.status, ("Неизвестно", "secondary"))

    @property
    def total_repair_duration(self):
        return sum(
            r.duration or 0 for r in self.repairs.all()
        )

    def __str__(self):
        return f"{self.name} ({self.inventory_number})"

    class Meta:
        ordering = ["-entry_date"]
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['inventory_number']),
            models.Index(fields=['name']),
        ]


class Repairers(models.Model):
    external_id = models.CharField(max_length=100, null=True, blank=True, unique=True)
    name = models.CharField(max_length=100, verbose_name="Название")
    address = models.CharField(max_length=300, verbose_name="Адрес", null=True, blank=True)
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    contact_person = models.CharField(max_length=100, verbose_name="Контактное лицо", null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    company_details = models.JSONField(default=dict, blank=True, verbose_name="Реквизиты")
    comment = models.CharField(max_length=300, verbose_name="Комментарий", null=True, blank=True)

    def __str__(self):
        return self.name


class Repairs(models.Model):
    external_id = models.CharField(max_length=100, null=True, blank=True, unique=True)
    instrument = models.ForeignKey(
        Instruments,
        on_delete=models.PROTECT,
        related_name="repairs",
        verbose_name="инструмент",
        null=True,
        blank=True,
    )
    repairer = models.ForeignKey(
        Repairers,
        on_delete=models.PROTECT,
        related_name="repair_done",
        verbose_name="исполнитель",
    )
    failure_date = models.DateField(verbose_name="Дата поломки")
    date_of_delivery_for_repair = models.DateField(verbose_name="Дата сдачи в ремонт")
    date_of_receipt_from_repair = models.DateField(
        blank=True, null=True, verbose_name="Дата получения из ремонта"
    )
    repair_cost = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        verbose_name="Стоимость ремонта",
        null=True,
        blank=True,
    )
    comment = models.TextField(verbose_name="Комментарий")

    def clean(self):
        super().clean()
        if self.failure_date and self.date_of_delivery_for_repair:
            if self.failure_date > self.date_of_delivery_for_repair:
                raise ValidationError({
                    'failure_date': 'Дата поломки не может быть позже даты сдачи в ремонт'
                })
        if self.date_of_delivery_for_repair and self.date_of_receipt_from_repair:
            if self.date_of_receipt_from_repair < self.date_of_delivery_for_repair:
                raise ValidationError({
                    'date_of_receipt_from_repair': 'Дата получения из ремонта не может быть раньше даты сдачи'
                })

    @property
    def duration(self):
        """Продолжительность ремонта в днях"""
        if self.date_of_receipt_from_repair:
            return (
                self.date_of_receipt_from_repair - self.date_of_delivery_for_repair
            ).days
        return None

    @property
    def is_active(self):
        """В ремонте или уже завершен"""
        return self.date_of_receipt_from_repair is None

    def save(self, *args, **kwargs):
        if not self.instrument:
            super().save(*args, **kwargs)
            return
        is_new = self.pk is None  # Сохраняем флаг ДО сохранения

        if not is_new:
            # Получаем старую версию записи
            try:
                old = Repairs.objects.get(pk=self.pk)
                # Если ремонт завершили (было null, стало не null)
                if old.date_of_receipt_from_repair is None and self.date_of_receipt_from_repair is not None:
                    self.instrument.status = Instruments.STATUS_IN_USE
                    self.instrument.save(update_fields=['status'])
            except Repairs.DoesNotExist:
                pass

        super().save(*args, **kwargs)

        # Если это новый ремонт
        if is_new and self.instrument and self.instrument.status != Instruments.STATUS_IN_REPAIR:
            self.instrument.status = Instruments.STATUS_IN_REPAIR
            self.instrument.save(update_fields=['status'])

    def __str__(self):
        return f"Ремонт #{self.id} - {self.instrument}"

    class Meta:
        ordering = ["-date_of_delivery_for_repair"]
        indexes = [
            models.Index(fields=['instrument', 'date_of_receipt_from_repair']),
        ]
        verbose_name = "Ремонт"
        verbose_name_plural = "Ремонты"


class Relocators(models.Model):
    """Ответственный за перемещение"""
    name = models.CharField(max_length=100,
                            verbose_name="ФИО")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ответственный за перемещение"
        verbose_name_plural = "Ответственные за перемещение"

class Relocations(models.Model):
    external_id = models.CharField(max_length=100, null=True, blank=True)
    instrument = models.ForeignKey(
        Instruments,
        on_delete=CASCADE,
        related_name="relocations",
        verbose_name="Инструмент"
    )
    comment = models.TextField(verbose_name="Комментарий")
    date = models.DateField(auto_now_add=True, verbose_name="Дата перемещения")
    relocator = models.ForeignKey(
        'Relocators',  # Используем строку для ссылки на модель, которая определена выше
        on_delete=models.PROTECT,
        related_name="relocations",
        verbose_name="Ответственный за перемещение",
        null=True,  # Добавьте null=True если поле может быть пустым
        blank=True
    )
    relocation_place = models.CharField(max_length=200, verbose_name='Куда перемещен')

    def clean(self):
        if self.instrument.status == Instruments.STATUS_RELOCATED and not self.comment:
            raise ValidationError({
                'comment': "Нужно указать комментарий для перемещенного инструмента (Причина перемещения)"
            })

        if self.instrument.status == Instruments.STATUS_IN_REPAIR:
            raise ValidationError({
                'instrument': "Нельзя переместить инструмент, который находится в ремонте"
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

        # Обновляем статус инструмента, если он еще не перемещен
        if self.instrument.status not in [Instruments.STATUS_RELOCATED, Instruments.STATUS_IN_REPAIR]:
            self.instrument.status = Instruments.STATUS_RELOCATED
            self.instrument.save(update_fields=['status'])

    def __str__(self):
        return f"Перемещение #{self.id}: {self.instrument} -> {self.relocation_place}"

    class Meta:
        verbose_name = "Перемещение"
        verbose_name_plural = "Перемещения"
        ordering = ["-date"]
