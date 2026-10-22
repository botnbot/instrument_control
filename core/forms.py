from django import forms

from core.models import Instrument, Repair, Repairer,  Relocation


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


class RelocationForm(forms.ModelForm):
    class Meta:
        model = Relocation
        fields = '__all__'

