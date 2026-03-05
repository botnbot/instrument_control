from django.contrib import admin

from core.models import Instruments, Repairers, Repairs


@admin.register(Instruments)
class InstrumentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'entry_date')
    search_fields = ('id', 'name', 'status', 'entry_date')


@admin.register(Repairers)
class RepairersAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Repairs)
class RepairsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'instrument', 'repairer', 'failure_date', 'date_of_delivery_for_repair',
        'date_of_receipt_from_repair','repair_cost',
    )
    search_fields = ('id', 'instrument__name', 'repairer__name',)
