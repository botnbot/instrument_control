import json

from django import forms

from core.models import Instruments, Repairs, Repairers, Relocations


class InstrumentsForm(forms.ModelForm):
    class Meta:
        model = Instruments
        fields = "__all__"
        widgets = {
            'entry_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'image1': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'image2': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'image3': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError('Цена не может быть отрицательной')
        return price

    def clean_inventory_number(self):
        inv_num = self.cleaned_data.get('inventory_number')
        if inv_num is not None and inv_num < 0:
            raise forms.ValidationError('Инвентарный номер не может быть отрицательным')
        return inv_num

    def clean_image1(self):
        image = self.cleaned_data.get('image1')
        if image and image.size > 5 * 1024 * 1024:
            raise forms.ValidationError('Размер изображения не должен превышать 5MB')
        return image


class RepairersForm(forms.ModelForm):
    company_details_json = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 6,
            'class': 'form-control font-monospace',
            'placeholder': '{\n  "inn": "3525234567",\n  "kpp": "352501001"\n}'
        }),
        required=False,
        help_text="Введите реквизиты в формате JSON"
    )

    class Meta:
        model = Repairers
        fields = "__all__"
        exclude = ("company_details",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.company_details:
            self.fields['company_details_json'].initial = json.dumps(
                self.instance.company_details,
                indent=2,
                ensure_ascii=False
            )

    def clean_company_details_json(self):
        data = self.cleaned_data.get('company_details_json', '').strip()
        if not data:
            return {}
        try:
            return json.loads(data)
        except json.JSONDecodeError as e:
            raise forms.ValidationError(f"Неверный формат JSON: {str(e)}")

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.company_details = self.cleaned_data.get('company_details_json', {})
        if commit:
            instance.save()
        return instance


class RepairsForm(forms.ModelForm):
    class Meta:
        model = Repairs
        fields = "__all__"
        widgets = {
            'instrument': forms.Select(attrs={'class': 'form-select select2'}),
            'failure_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_of_delivery_for_repair': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_of_receipt_from_repair': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'repair_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'comment': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        failure_date = cleaned_data.get('failure_date')
        delivery_date = cleaned_data.get('date_of_delivery_for_repair')
        receipt_date = cleaned_data.get('date_of_receipt_from_repair')

        if failure_date and delivery_date and failure_date > delivery_date:
            raise forms.ValidationError('Дата поломки не может быть позже даты сдачи в ремонт')

        if delivery_date and receipt_date and receipt_date < delivery_date:
            raise forms.ValidationError('Дата получения из ремонта не может быть раньше даты сдачи')

        return cleaned_data

    def clean_instrument(self):
        instrument = self.cleaned_data.get('instrument')
        if not instrument:
            return instrument

        # Проверяем, нет ли уже активного ремонта
        active_repair = Repairs.objects.filter(
            instrument=instrument,
            date_of_receipt_from_repair__isnull=True
        ).exclude(pk=self.instance.pk if self.instance else None).first()

        if active_repair:
            raise forms.ValidationError(
                f'Инструмент уже находится в ремонте (ремонт #{active_repair.id}). '
                f'Сначала завершите текущий ремонт.'
            )

        return instrument


class RelocationsForm(forms.ModelForm):
    class Meta:
        model = Relocations
        fields = "__all__"
        widgets = {
            'instrument': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }