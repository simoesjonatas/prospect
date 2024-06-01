from datetime import datetime
from django.db import models
from django.urls import reverse
from .cliente import Cliente
from calendarapp.models import EventAbstract
from accounts.models import User


class EventManager(models.Manager):
    """ Event manager """

    def get_all_events(self, user):
        # events = Event.objects.filter(user=user, is_active=True, is_deleted=False)
        # return events
        if user.is_staff:
            events = Event.objects.filter(is_active=True,is_deleted=False)
        else:
            # Obtém a lista de clientes do usuário
            ListaDeClientes = Cliente.objects.filter(usuario_designado=user)
            # Extrai os IDs dos clientes da lista de clientes
            ListaDeClientesIDs = ListaDeClientes.values_list('id', flat=True)
            # Filtra os eventos com base nos IDs dos clientes
            events = Event.objects.filter(cliente__id__in=ListaDeClientesIDs, is_active=True, is_deleted=False)
            # events = Event.objects.filter(user=user, is_active=True, is_deleted=False)
        return events

    def get_running_events(self, user):
        if user.is_staff:
            running_events = Event.objects.filter(
                is_active=True,
                is_deleted=False,
                end_time__gte=datetime.now().date(),
            ).order_by("start_time")
        else:
            ListaDeClientes = Cliente.objects.filter(usuario_designado=user)
            # Extrai os IDs dos clientes da lista de clientes
            ListaDeClientesIDs = ListaDeClientes.values_list('id', flat=True)
            running_events = Event.objects.filter(
                cliente__id__in=ListaDeClientesIDs,
                is_active=True,
                is_deleted=False,
                end_time__gte=datetime.now().date(),
            ).order_by("start_time")
        return running_events


class Event(EventAbstract):
    """ Event model """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=200)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    objects = EventManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("calendarapp:event-detail", args=(self.id,))
    
    def delete(self, *args, **kwargs):
        # Marcar como não ativo e deletado em vez de excluir
        self.is_active = False
        self.is_deleted = True
        self.save()

    @property
    def get_html_url(self):
        url = reverse("calendarapp:event-detail", args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'
