from django.urls import path
from .views import event_list, event_create, event_update,event_delete,event_detail,dashboard,filter_events,search_events,event_statistics,category_list,category_create,category_update,category_delete, event_stats

from . import views

urlpatterns = [
    path('', event_list, name='event_list'),
    path('create/', event_create, name='event_create'),
    path('<int:pk>/edit/', event_update, name='event_update'),
    path('<int:pk>/delete/', event_delete, name='event_delete'),
    path('<int:pk>/', event_detail, name='event_detail'),
    path('dashboard/', dashboard, name='dashboard'),
    path('filter/<str:event_type>/', filter_events, name='filter_events'),
    path('search/', search_events, name='search_events'),
    path('statistics/', event_statistics, name='event_statistics'),
    path('categories/', category_list, name='category_list'),
    path('categories/new/', category_create, name='category_create'),
    path('categories/<int:pk>/edit/', category_update, name='category_update'),
    path('categories/<int:pk>/delete/', category_delete, name='category_delete'),
    path('stats/', event_stats, name='event_stats'),

]
