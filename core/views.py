from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, ListView, DeleteView

from .forms import InstrumentsForm, RepairersForm, RepairsForm
from .models import Instruments, Repairers, Repairs
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "home.html"



class InstrumentsCreateView(CreateView):
    model = Instruments
    form_class = InstrumentsForm
    template_name = 'core/instruments/instruments_form.html'
    success_url = reverse_lazy("core:instrument")
    context_object_name = 'instrument'


class InstrumentsDetailView(DetailView):
    model = Instruments
    template_name = "core/instruments/detail.html"
    context_object_name = 'instrument'


class InstrumentsListView(ListView):
    model = Instruments
    template_name = 'core/instruments/instrument_list.html'
    context_object_name = 'instruments'


class InstrumentsUpdateView(UpdateView):
    model = Instruments
    form_class = InstrumentsForm
    template_name = 'core/instruments/instruments_form.html'

    def get_success_url(self):
        return reverse_lazy('core:instrument_detail', kwargs={'pk': self.object.pk})


class InstrumentsDeleteView(DeleteView):
    model = Instruments
    template_name = 'core/instruments/instruments_confirm_delete.html'
    success_url = reverse_lazy("core:instrument_list")


class RepairersCreateView(CreateView):
    model = Repairers
    form_class = RepairersForm
    success_url = reverse_lazy('core:repairers_list')
    template_name = 'core:repairers/repairers_form.html'
    context_object_name = 'repairer'


class RepairsCreateView(CreateView):
    model = Repairs
    form_class = RepairsForm
    success_url = reverse_lazy('core:repairers_list')
    context_object_name = 'repair'


class RepairersListView(ListView):
    model = Repairers
    template_name = 'core/repairers/repairer_list.html'
    context_object_name = 'repairers'


class RepairsListView(ListView):
    model = Repairs
    template_name = 'core/repairs/repair_list.html'
    context_object_name = 'repairs'


