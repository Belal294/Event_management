from django.urls import path
from .views import event_list, event_create, event_delete, event_update, event_detail, filter_events, upcoming_events,search_events, category_create, category_list, category_update, category_delete
from . import views

urlpatterns = [
    path('', event_list, name='event_list'),  
    path('create/', event_create, name='event_create'),
    path('<int:pk>/edit/', event_update, name='event_update'),
    path('<int:pk>/delete/', event_delete, name='event_delete'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('<int:pk>/', event_detail, name='event_detail'),
    path('filter/<str:event_type>/', filter_events, name='filter_events'),
    path('filter/upcoming/', upcoming_events, name='upcoming_events'),
    path('search/', search_events, name='search_events'),
    path('categories/', category_list, name='category_list'),
    path('categories/new/', category_create, name='category_create'),
    path('categories/<int:pk>/edit/', category_update, name='category_update'),
    path('categories/<int:pk>/delete/', category_delete, name='category_delete'),
]
