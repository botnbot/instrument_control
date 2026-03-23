from django import forms

from core.models import Instruments, Repairs, Repairers, Relocations


class InstrumentsForm(forms.ModelForm):
    class Meta:
        model = Instruments
        fields = "__all__"


class RepairersForm(forms.ModelForm):
    class Meta:
        model = Repairers
        fields = "__all__"


class RepairsForm(forms.ModelForm):
    class Meta:
        model = Repairs
        fields = "__all__"
        widgets = {
            'instrument': forms.Select(attrs={'class': 'form-select select2'}),
            'failure_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'date_of_delivery_for_repair': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'date_of_receipt_from_repair': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
        }


class RelocationsForm(forms.ModelForm):
    class Meta:
        model = Relocations
        fields = "__all__"
