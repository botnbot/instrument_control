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


class RelocationsForm(forms.ModelForm):
    class Meta:
        model = Relocations
        fields = "__all__"
