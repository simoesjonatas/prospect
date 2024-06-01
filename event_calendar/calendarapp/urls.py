from django.urls import path, include

from . import views

app_name = "calendarapp"


urlpatterns = [
    path("calender/", views.CalendarViewNew.as_view(), name="calendar"),
    path("calenders/", views.CalendarView.as_view(), name="calendars"),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('next_week/<int:event_id>/', views.next_week, name='next_week'),
    path('next_day/<int:event_id>/', views.next_day, name='next_day'),
    path("event/new/", views.create_event, name="event_new"),
    path("event/edit/<int:pk>/", views.EventEdit.as_view(), name="event_edit"),
    path("event/<int:event_id>/details/", views.event_details, name="event-detail"),
    
    path("client/new/", views.create_cliente, name="client_new"),
    path("client/edit/<int:pk>/", views.ClienteEdit.as_view(), name="client_edit"),
    path("client/<int:cliente_id>/details/", views.client_details, name="client-detail"),
    path('cliente/<int:cliente_id>/criar_evento/', views.criar_evento_cliente, name='criar_evento_cliente'),

    
    path("status/new/", views.create_status, name="status_new"),
    path("status/edit/<int:pk>/", views.StatusEdit.as_view(), name="status_edit"),
    path("status/<int:status_id>/details/", views.status_details, name="status-detail"),
    
    path("canal/new/", views.create_canal, name="canal_new"),
    path("canal/edit/<int:pk>/", views.CanalEdit.as_view(), name="canal_edit"),
    path("canal/<int:canal_id>/details/", views.canal_details, name="canal-detail"),
    
    path(
        "add_eventmember/<int:event_id>", views.add_eventmember, name="add_eventmember"
    ),
    path(
        "event/<int:pk>/remove",
        views.EventMemberDeleteView.as_view(),
        name="remove_event",
    ),
    path("all-client-list/", views.AllClientesListView.as_view(), name="all_clients"),
    path("all-canal-list/", views.AllCanalListView.as_view(), name="all_canal"),
    path("all-status-list/", views.AllStatusListView.as_view(), name="all_status"),
    path("all-event-list/", views.AllEventsListView.as_view(), name="all_events"),
    path(
        "running-event-list/",
        views.RunningEventsListView.as_view(),
        name="running_events",
    ),
]
