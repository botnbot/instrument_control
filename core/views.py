from django.db.models import Q
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView, UpdateView, ListView, DeleteView

from .forms import InstrumentsForm, RepairersForm, RepairsForm
from .models import Instruments, Repairers, Repairs
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "home.html"


# ________________________________Instruments_____________________________________________
class InstrumentsCreateView(CreateView):
    model = Instruments
    form_class = InstrumentsForm
    template_name = 'core/instruments/instruments_form.html'
    success_url = reverse_lazy("core:instrument_list")


class InstrumentsDetailView(DetailView):
    model = Instruments
    template_name = "core/instruments/detail.html"
    context_object_name = 'instrument'


class InstrumentsListView(ListView):
    model = Instruments
    template_name = 'core/instruments/instrument_list.html'
    context_object_name = 'instruments'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            qs = qs.filter(
                Q(name__icontains=search_query )|
                Q(inventory_number__icontains=search_query)
                           )
        return qs


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


# ________________________________Repairers_____________________________________________
class RepairersCreateView(CreateView):
    model = Repairers
    form_class = RepairersForm
    template_name = 'core/repairers/repairers_form.html'
    success_url = reverse_lazy('core:repairer_list')


class RepairersDetailView(DetailView):
    model = Repairers
    template_name = "core/repairers/detail.html"
    context_object_name = 'repairer'


class RepairersListView(ListView):
    model = Repairers
    template_name = 'core/repairers/repairer_list.html'
    context_object_name = 'repairers'
    paginate_by = 10


class RepairersUpdateView(UpdateView):
    model = Repairers
    form_class = RepairersForm
    template_name = 'core/repairers/repairers_form.html'

    def get_success_url(self):
        return reverse_lazy('core:repairer_detail', kwargs={'pk': self.object.pk})


class  RepairersDeleteView(DeleteView):
    model = Repairers
    template_name = 'core/repairers/repairer_confirm_delete.html'
    success_url = reverse_lazy("core:repairer_list")


# ________________________________Repairs____________________________________________
class RepairsCreateView(CreateView):
    model = Repairs
    form_class = RepairsForm
    template_name = 'core/repairs/repairs_form.html'
    success_url = reverse_lazy('core:repair_list')
    context_object_name = 'repair'


class RepairsDetailView(DetailView):
    model = Repairs
    template_name = "core/repairs/detail.html"
    context_object_name = 'repairs'


class RepairsListView(ListView):
    model = Repairs
    template_name = 'core/repairs/repair_list.html'
    context_object_name = 'repairs'
    paginate_by = 10


class RepairsUpdateView(UpdateView):
    model = Repairs
    form_class = RepairsForm
    template_name = 'core/repairs/repairs_form.html'

    def get_success_url(self):
        return reverse_lazy('core:repair_detail', kwargs={'pk': self.object.pk})


class RepairsDeleteView(DeleteView):
    model = Repairs
    template_name = 'core/repairs/repair_confirm_delete.html'
    success_url = reverse_lazy("core:repair_list")


class SendForRepairView(CreateView):
    model = Repairs
    fields = ["repairer", "comment", "failure_date"]
    template_name = "core/repairs/send_for_repair.html"
    success_url = reverse_lazy("core:repair_list")

    def form_valid(self, form):
        instrument = Instruments.objects.get(pk=self.kwargs["pk"])
        form.instance.instrument = instrument
        form.instance.date_of_delivery_for_repair = timezone.now().date()
        return super().form_valid(form)

