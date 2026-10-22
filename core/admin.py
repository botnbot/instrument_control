from django.contrib import admin
from core.models import Instrument, Repairer, Repair, Relocation


@admin.register(Instrument)
class InstrumentsAdmin(admin.ModelAdmin):
    list_display = ('inventory_N', 'name', 'status', 'price', 'entry_date', 'is_new')
    list_display_links = ('inventory_N', 'name')
    list_filter = ('status', 'is_new', 'entry_date')
    search_fields = ('name', 'inventory_N', 'comment')


@admin.register(Repairer)
class RepairerAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'phone')
    search_fields = ('name', 'contact_person', 'phone')


@admin.register(Repair)
class RepairAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'instrument', 'repairer', 'failure_date', 'date_of_delivery_for_repair',
        'date_of_receipt_from_repair', 'repair_cost', 'duration_display'  # <-- ДОБАВЛЕНО
    )
    list_filter = ('failure_date', 'date_of_delivery_for_repair', 'repairer')  # <-- ДОБАВЛЕНО
    search_fields = ('id', 'instrument__name', 'repairer__name', 'comment')

    # Вспомогательный метод для отображения duration в списке
    @admin.display(description='Дней в ремонте')
    def duration_display(self, obj):
        return obj.duration


# ДОБАВЛЕНА МОДЕЛЬ ПЕРЕМЕЩЕНИЙ
@admin.register(Relocation)
class RelocationAdmin(admin.ModelAdmin):
    list_display = ('instrument', 'location', 'date', 'comment')
    list_filter = ('date',)
    search_fields = ('instrument__name', 'location', 'comment')
    autocomplete_fields = ('instrument',)  # Удобный поиск инструмента