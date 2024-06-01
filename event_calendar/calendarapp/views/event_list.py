from django.views.generic import ListView

from calendarapp.models import Event
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class AllEventsListView(ListView):
    """ All event list views """

    template_name = "event/events_list.html"
    model = Event

    def get_queryset(self):
        return Event.objects.get_all_events(user=self.request.user)

@method_decorator(login_required, name='dispatch')
class RunningEventsListView(ListView):
    """ Running events list view """

    template_name = "event/events_list.html"
    model = Event

    def get_queryset(self):
        return Event.objects.get_running_events(user=self.request.user)
