from django.urls import path

from events.api import views

app_name = 'events'

urlpatterns = [
    path('events/', views.ListEventsApiView.as_view(), name='api-list-events'),
    path('event/<id>', views.UpdateEventApiView.as_view(), name='api-subscribe-event'),

]
