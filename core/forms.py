from django import forms

from .models import Repair, Instrument, Repairer, Relocation


class InstrumentForm(forms.ModelForm):
    class Meta:
        model = Instrument
        fields = '__all__'


class RepairerForm(forms.ModelForm):
    class Meta:
        model = Repairer
        fields = '__all__'


class RepairForm(forms.ModelForm):
    class Meta:
        model = Repair
        fields = '__all__'
        widgets = {
            # Скрываем стандартный выпадающий список для инструмента
            'instrument': forms.HiddenInput(),

            # Красиво оформляем остальные поля (даты, суммы, текст)
            'failure_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_of_delivery_for_repair': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_of_receipt_from_repair': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'repair_cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            # Для ремонтника оставляем выпадающий список, но с красивым стилем
            'repairer': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Делаем поле инструмента необязательным на уровне HTML (чтобы браузер не ругался),
        # так как его заполняет наш JavaScript
        self.fields['instrument'].required = False


class RelocationForm(forms.ModelForm):
    class Meta:
        model = Relocation
        fields = '__all__'
