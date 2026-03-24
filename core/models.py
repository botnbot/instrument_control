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
    external_id = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name="Наименование")
    inventory_number = models.IntegerField(
        unique=True,
        null=True,
        blank=True,
        verbose_name="Инвентарный номер",
    )
    entry_date = models.DateField(verbose_name="Дата ввода")
    price = models.DecimalField(decimal_places=2, max_digits=8, verbose_name="Цена")
    is_new = models.BooleanField(default=True)
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

    def __str__(self):
        return f"{self.name} ({self.inventory_number})"

    class Meta:
        ordering = ["-entry_date"]


class Repairers(models.Model):
    external_id = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name="Название")
    address = models.CharField(max_length=300, verbose_name="Адрес", null=True, blank=True)
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    contact_person = models.CharField(max_length=100, verbose_name="Контактное лицо", null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    company_details = models.CharField(max_length=100, blank=True, verbose_name="Реквизиты")
    comment = models.CharField(max_length=300, verbose_name="Коментарий", null=True, blank=True)

    def __str__(self):
        return self.name


class Repairs(models.Model):
    external_id = models.CharField(max_length=100, null=True, blank=True)
    instrument = models.ForeignKey(
        Instruments,
        on_delete=models.CASCADE,
        related_name="repairs",
        verbose_name="инструмент",
        null=True,
        blank=True,
    )
    repairer = models.ForeignKey(
        Repairers,
        on_delete=models.CASCADE,
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

    @property
    def duration(self):
        if self.date_of_receipt_from_repair:
            return (
                self.date_of_receipt_from_repair - self.date_of_delivery_for_repair
            ).days
        return None

    class Meta:
        ordering = ["-date_of_delivery_for_repair"]


class Relocator(models.Model):
    pass


class Relocations(models.Model):
    external_id = models.CharField(max_length=100, null=True, blank=True)
    instrument = models.ForeignKey(
        Instruments, on_delete=CASCADE, related_name="relocations"
    )
    comment = models.TextField()
    date = models.DateField(auto_now_add=True)

    def clean(self):
        if self.instrument.status == Instruments.STATUS_RELOCATED and not self.comment:
            raise ValidationError(
                "Нужно указать комментарий для перемещенного инструмента"
            )
