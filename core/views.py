from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .forms import InstrumentForm, RepairerForm, RepairForm, RelocationForm
from .models import Instrument, Repairer, Repair, Relocation


# === Инструменты ===
class InstrumentListView(ListView):
    model = Instrument
    template_name = 'core/instruments/instrument_list.html'
    context_object_name = 'instruments'
    paginate_by = 10


class InstrumentDetailView(DetailView):
    model = Instrument
    template_name = 'core/instruments/instrument_detail.html'
    context_object_name = 'instrument'


class InstrumentCreateView(LoginRequiredMixin, CreateView):
    model = Instrument
    form_class = InstrumentForm
    template_name = 'core/instruments/instruments_form.html'
    success_url = reverse_lazy('core:instrument_list')

    def form_valid(self, form):
        messages.success(self.request, "Инструмент успешно добавлен.")
        return super().form_valid(form)


class InstrumentUpdateView(LoginRequiredMixin, UpdateView):
    model = Instrument
    form_class = InstrumentForm
    template_name = 'core/instruments/instruments_form.html'
    success_url = reverse_lazy('core:instrument_list')


class InstrumentDeleteView(LoginRequiredMixin, DeleteView):
    model = Instrument
    template_name = 'core/instruments/instrument_confirm_delete.html'
    success_url = reverse_lazy('core:instrument_list')


# === Ремонтники ===
class RepairerListView(ListView):
    model = Repairer
    template_name = 'core/repairers/repairers_list.html'
    context_object_name = 'repairers'


class RepairerDetailView(DetailView):  # <- ЭТОТ КЛАСС ВЫ ПРОПУСТИЛИ
    model = Repairer
    template_name = 'core/repairers/repairers_detail.html'
    context_object_name = 'repairer'


class RepairerCreateView(LoginRequiredMixin, CreateView):
    model = Repairer
    form_class = RepairerForm
    template_name = 'core/repairers/repairers_form.html'
    success_url = reverse_lazy('core:repairer_list')


class RepairerUpdateView(LoginRequiredMixin, UpdateView):
    model = Repairer
    form_class = RepairerForm
    template_name = 'core/repairers/repairers_form.html'
    success_url = reverse_lazy('core:repairer_list')


# === Ремонты ===
class RepairListView(ListView):
    model = Repair
    template_name = 'core/repairs/repairs_list.html'
    context_object_name = 'repairs'


class RepairDetailView(DetailView):
    model = Repair
    template_name = 'core/repairs/repairs_detail.html'
    context_object_name = 'repair'


class RepairCreateView(LoginRequiredMixin, CreateView):
    model = Repair
    form_class = RepairForm
    template_name = 'core/repairs/repairs_form.html'
    success_url = reverse_lazy('core:repair_list')


class RepairUpdateView(LoginRequiredMixin, UpdateView):
    model = Repair
    form_class = RepairForm
    template_name = 'core/repairs/repairs_form.html'
    success_url = reverse_lazy('core:repair_list')


# === Перемещения ===
class RelocationListView(ListView):
    model = Relocation
    template_name = 'core/relocations/relocations_list.html'
    context_object_name = 'relocations'


class RelocationCreateView(LoginRequiredMixin, CreateView):
    model = Relocation
    form_class = RelocationForm
    template_name = 'core/relocations/relocations_form.html'
    success_url = reverse_lazy('core:relocation_list')