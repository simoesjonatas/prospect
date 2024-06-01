from django.views.generic import ListView
from calendarapp.models import Cliente, Status
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class AllClientesListView(ListView):
    """ All cliente list views """

    template_name = "cliente/cliente_list.html"
    model = Cliente
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtém a lista de status do seu sistema
        context['status_choices'] = Status.objects.all()
        status_filter = self.request.GET.get('status_filter')
        context['selected_status'] = int(status_filter) if status_filter else None
        
        return context
    
    def get_queryset(self):
        # return Cliente.objects.all()
        queryset = Cliente.objects.get_all_clients(user=self.request.user)

        status_filter = self.request.GET.get('status_filter')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset

