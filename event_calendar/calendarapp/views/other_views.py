# cal/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe
from datetime import timedelta, datetime, date
import calendar
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from calendarapp.models import EventMember, Event, Cliente, Status, CanalMarket
from calendarapp.utils import Calendar
from calendarapp.forms import EventForm, AddMemberForm, ClienteForm, StatusForm, CanalForm


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = "month=" + str(next_month.year) + "-" + str(next_month.month)
    return month


class CalendarView(LoginRequiredMixin, generic.ListView):
    login_url = "accounts:signin"
    model = Event
    template_name = "calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get("month", None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context["calendar"] = mark_safe(html_cal)
        context["prev_month"] = prev_month(d)
        context["next_month"] = next_month(d)
        return context

@login_required(login_url="accounts:signin")
def criar_evento_cliente(request, cliente_id):
    cliente = Cliente.objects.get(pk=cliente_id)
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            cliente = form.cleaned_data["cliente"]
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            start_time = form.cleaned_data["start_time"]
            end_time = form.cleaned_data["end_time"]
            Event.objects.get_or_create(
                cliente=cliente,
                user=request.user,
                title=title,
                description=description,
                start_time=start_time,
                end_time=end_time,
            )
            return redirect('calendarapp:client-detail', cliente_id=cliente_id)
    else:
        form = EventForm()
    return render(request, 'event.html', {'form': form, 'cliente': cliente})

@login_required(login_url="accounts:signin")
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, user=request.user)  # Passando o usuário para o formulário
        if form.is_valid():
            cliente = form.cleaned_data["cliente"]
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            start_time = form.cleaned_data["start_time"]
            end_time = form.cleaned_data["end_time"]
            Event.objects.create(
                cliente=cliente,
                user=request.user,
                title=title,
                description=description,
                start_time=start_time,
                end_time=end_time,
            )
            return HttpResponseRedirect(reverse("calendarapp:calendar"))
    else:
        form = EventForm(user=request.user)  # Passando o usuário para o formulário
    return render(request, "event/event.html", {"form": form})

# @login_required(login_url="accounts:signin")
# def create_event(request):
#     form = EventForm(request.POST or None)
#     if request.POST and form.is_valid():
#         cliente = form.cleaned_data["cliente"]
#         title = form.cleaned_data["title"]
#         description = form.cleaned_data["description"]
#         start_time = form.cleaned_data["start_time"]
#         end_time = form.cleaned_data["end_time"]
#         Event.objects.get_or_create(
#             cliente=cliente,
#             user=request.user,
#             title=title,
#             description=description,
#             start_time=start_time,
#             end_time=end_time,
#         )
#         return HttpResponseRedirect(reverse("calendarapp:calendar"))
#     return render(request, "event.html", {"form": form})


class EventEdit(generic.UpdateView):
    # model = Event
    # fields = ["title", "description","cliente", "start_time", "end_time"]
    # template_name = "event/event.html"
    model = Event
    form_class = EventForm  # Use o formulário personalizado EventForm
    template_name = "event/event.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Passe o usuário atual para o formulário
        return kwargs


@login_required(login_url="accounts:signin")
def create_canal(request):
    form = CanalForm(request.POST or None)
    if request.POST and form.is_valid():
        nome = form.cleaned_data["nome"]
        CanalMarket.objects.get_or_create(
            nome = nome,
        )
        return HttpResponseRedirect(reverse("calendarapp:all_canal"))
    return render(request, "canal/canal.html", {"form": form})


class CanalEdit(generic.UpdateView):
    model = CanalMarket
    fields = ["nome"]
    template_name = "canal/canal.html"


@login_required(login_url="accounts:signin")
def canal_details(request, canal_id):
    event = CanalMarket.objects.get(id=canal_id)
    context = {"event": event}
    return render(request, "canal/canal-details.html", context)


@login_required(login_url="accounts:signin")
def create_status(request):
    form = StatusForm(request.POST or None)
    if request.POST and form.is_valid():
        nome = form.cleaned_data["nome"]
        Status.objects.get_or_create(
            nome = nome,
        )
        return HttpResponseRedirect(reverse("calendarapp:all_status"))
    return render(request, "status/status.html", {"form": form})


class StatusEdit(generic.UpdateView):
    model = Status
    fields = ["nome"]
    template_name = "status/status.html"


@login_required(login_url="accounts:signin")
def status_details(request, status_id):
    event = Status.objects.get(id=status_id)
    context = {"event": event}
    return render(request, "status/status-details.html", context)

@login_required(login_url="accounts:signin")
def create_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST, user=request.user)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.save(user=request.user)
            return redirect('calendarapp:all_clients')
    else:
        form = ClienteForm(user=request.user)
    
    return render(request, "cliente/cliente.html", {"form": form})



class ClienteEdit(LoginRequiredMixin, generic.UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "cliente/cliente.html"
    success_url = reverse_lazy('calendarapp:client-detail')
    login_url = 'accounts:signin'

    def form_valid(self, form):
        cliente = form.save(commit=False)
        cliente.save(user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_success_url(self):
        return reverse_lazy('calendarapp:client-detail', kwargs={'cliente_id': self.object.pk})



# class ClienteEdit(generic.UpdateView):
#     model = Cliente
#     # fields = ["nome", "telefone", "email", "status",]
#     # template_name = "cliente/cliente.html"
#     form_class = ClienteForm
#     template_name = "cliente/cliente.html"

#     def get_success_url(self):
#         return reverse_lazy('calendarapp:client-detail', kwargs={'cliente_id': self.object.pk})

#     def get_form_kwargs(self):
#         kwargs = super(ClienteEdit, self).get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs


@login_required(login_url="accounts:signin")
def client_details(request, cliente_id):
    event = Cliente.objects.get(id=cliente_id)
    eventmember = Event.objects.filter(cliente=cliente_id)
    context = {"event": event, "eventmember": eventmember}
    return render(request, "cliente/cliente-details.html", context)


@login_required(login_url="accounts:signin")
def event_details(request, event_id):
    event = Event.objects.get(id=event_id)
    eventmember = EventMember.objects.filter(event=event)
    context = {"event": event, "eventmember": eventmember}
    return render(request, "event/event-details.html", context)


def add_eventmember(request, event_id):
    forms = AddMemberForm()
    if request.method == "POST":
        forms = AddMemberForm(request.POST)
        if forms.is_valid():
            member = EventMember.objects.filter(event=event_id)
            event = Event.objects.get(id=event_id)
            if member.count() <= 9:
                user = forms.cleaned_data["user"]
                EventMember.objects.create(event=event, user=user)
                return redirect("calendarapp:calendar")
            else:
                print("--------------User limit exceed!-----------------")
    context = {"form": forms}
    return render(request, "add_member.html", context)


class EventMemberDeleteView(generic.DeleteView):
    model = EventMember
    template_name = "event_delete.html"
    success_url = reverse_lazy("calendarapp:calendar")

class CalendarViewNew(LoginRequiredMixin, generic.View):
    login_url = "accounts:signin"
    template_name = "calendarapp/calendar.html"
    form_class = EventForm

    def get(self, request, *args, **kwargs):
        forms = self.form_class(user=request.user)
        events = Event.objects.get_all_events(user=request.user)
        events_month = Event.objects.get_running_events(user=request.user)
        event_list = []
        # start: '2020-09-16T16:00:00'
        for event in events:
            event_list.append(
                {   "id": event.id,
                    "title": event.title,
                    "cliente": event.cliente.nome,
                    "criadorEvento": event.user.email,
                    "clienteId": event.cliente.id,
                    "start": event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "end": event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "description": event.description,
                }
            )
        
        context = {"form": forms, "events": event_list,
                   "events_month": events_month}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            form = forms.save(commit=False)
            form.user = request.user
            form.save()
            return redirect("calendarapp:calendar")
        context = {"form": forms}
        return render(request, self.template_name, context)



def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        return JsonResponse({'message': 'Event sucess delete.'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)

def next_week(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        next = event
        next.id = None
        next.start_time += timedelta(days=7)
        next.end_time += timedelta(days=7)
        next.save()
        return JsonResponse({'message': 'Sucess!'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)

def next_day(request, event_id):

    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        next = event
        next.id = None
        next.start_time += timedelta(days=1)
        next.end_time += timedelta(days=1)
        next.save()
        return JsonResponse({'message': 'Sucess!'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)
