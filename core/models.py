from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import CASCADE


# Create your models here.


class Instruments(models.Model):
    STATUS_IN_USE = 'IN_USE'
    STATUS_REPAIRED = 'REPAIRED'
    STATUS_RELOCATED = 'RELOCATED'
    STATUS_BROKEN = 'BROKEN'

    STATUS_CHOICES = [
        (STATUS_IN_USE, "в работе"),
        (STATUS_REPAIRED, "в ремонте"),
        (STATUS_RELOCATED, "перемещен"),
        (STATUS_BROKEN, "сломан"),
    ]
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
    image1 = models.ImageField(upload_to="instruments/foto", verbose_name="Фото инструмента1")
    image2 = models.ImageField(upload_to="instruments/foto", verbose_name="Фото инструмента2", blank=True)
    image3 = models.ImageField(upload_to="instruments/foto", verbose_name="Фото инструмента3", blank=True)
    comment = models.TextField(max_length=200, verbose_name="Комментарий")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=STATUS_IN_USE)

    def __str__(self):
        return self.name


class Repairers(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    address = models.CharField(max_length=300, verbose_name="Адрес")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    contact_person = models.CharField(max_length=100, verbose_name="Контактное лицо")
    email = models.EmailField()
    comment = models.CharField(max_length=300, verbose_name="Коментарий")

    def __str__(self):
        return self.name


class Repairs(models.Model):
    instrument = models.ForeignKey(Instruments, on_delete=models.CASCADE, related_name='repairs',
                                   verbose_name='инструмент', null=True,
                                   blank=True)
    repairer = models.ForeignKey(Repairers, on_delete=models.PROTECT, related_name='repair_done',
                                 verbose_name='исполнитель')
    failure_date = models.DateField(verbose_name='Дата поломки')
    date_of_delivery_for_repair = models.DateField(verbose_name="Дата сдачи в ремонт")
    date_of_receipt_from_repair = models.DateField(blank=True, null=True, verbose_name="Дата получения из ремонта")
    repair_cost = models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Стоимость ремонта")
    comment = models.TextField(verbose_name="Комментарий")

    @property
    def duration(self):
        if self.date_of_receipt_from_repair:
            return (self.date_of_receipt_from_repair - self.date_of_delivery_for_repair).days
        return None


class Relocator(models.Model):
    pass


class Relocations(models.Model):
    instrument = models.ForeignKey(Instruments, on_delete=CASCADE, related_name='relocations')
    comment = models.TextField()
    date = models.DateField(auto_now_add=True)

    def clean(self):
        if self.instrument.status == Instruments.STATUS_RELOCATED and not self.comment:
            raise ValidationError("Нужно указать комментарий для перемещенного инструмента")
