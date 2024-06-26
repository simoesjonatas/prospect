from .event_list import AllEventsListView, RunningEventsListView
from .other_views import (
    CalendarViewNew,
    CalendarView,
    create_cliente,
    create_canal,
    create_event,
    criar_evento_cliente,
    create_status,
    CanalEdit,
    ClienteEdit,
    EventEdit,
    canal_details,
    client_details,
    event_details,
    add_eventmember,
    EventMemberDeleteView,
    delete_event,
    next_week,
    next_day,
    status_details,
    StatusEdit,
)
from .client_list import AllClientesListView
from .status_list import AllStatusListView
from .canal_list import AllCanalListView


__all__ = [
    AllCanalListView,
    AllClientesListView,
    AllEventsListView,
    AllStatusListView,
    RunningEventsListView,
    CalendarViewNew,
    CalendarView,
    create_canal,
    create_cliente,
    criar_evento_cliente,
    CanalEdit,
    canal_details,
    create_event,
    client_details,
    create_status,
    ClienteEdit,
    EventEdit,
    event_details,
    add_eventmember,
    EventMemberDeleteView,
    delete_event,
    next_week,
    next_day,
    status_details,
    StatusEdit,
]
