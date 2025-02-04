from django.urls import path
from .views import event_list, event_create, event_delete, event_update, event_detail, filter_events, upcoming_events,search_events
from . import views

urlpatterns = [
    path('', event_list, name='event_list'),  # Home page with list of events
    path('create/', event_create, name='event_create'),
    path('<int:pk>/edit/', event_update, name='event_update'),  # Event edit page
    path('<int:pk>/delete/', event_delete, name='event_delete'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('<int:pk>/', event_detail, name='event_detail'),  # Event detail page
    path('filter/<str:event_type>/', filter_events, name='filter_events'),
    path('filter/upcoming/', upcoming_events, name='upcoming_events'),
    path('search/', search_events, name='search_events'),
]
