from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    event_stats, filter_events, search_events, manage_events, rsvp_event, cancel_rsvp, dashboard, total_events, total_participants, upcoming_events, past_events,
    EventListView, CreateEvent, EventUpdateView, EventDeleteView, EventDetailView,
    CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView, ParticipantListView, ParticipantCreateView, ParticipantDeleteView,
    
)
from users.views import sign_up, sign_in, sign_out, signup_view, admin_dashboard

urlpatterns = [
    #  Authentication URLs
    path('sign-up/', sign_up, name='sign-up'),
    path('login/', sign_in, name='login'),
    path('logout/', sign_out, name='logout'),
    path("signup/", signup_view, name="signup"),

    # Django built-in authentication views
    path("auth-login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="auth-login"),
    path("auth-logout/", auth_views.LogoutView.as_view(), name="auth-logout"),

    #  Dashboard
    path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('dashboard/', dashboard, name='dashboard'),

    #  Event URLs
    path('events/', EventListView.as_view(), name='event_list'),
    path('events/create/', CreateEvent.as_view(), name='event_create'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('events/update/<int:pk>/', EventUpdateView.as_view(), name='event_update'),
    path('events/delete/<int:pk>/', EventDeleteView.as_view(), name='event_delete'),

   # Event Statistics & Filtering
    path('events/stats/', event_stats, name='event_stats'),
    path('events/filter/<str:event_type>/', filter_events, name='filter_events'),
    path('events/search/', search_events, name='search_events'),
    path('events/<int:event_id>/rsvp/', rsvp_event, name='rsvp_event'),
    path('events/<int:event_id>/cancel_rsvp/', cancel_rsvp, name='cancel_rsvp'),

    # Show Statistics
    path('total-events/', total_events, name='total_events'),
    path('total-participants/', total_participants, name='total_participants'),
    path('upcoming-events/', upcoming_events, name='upcoming_events'),
    path('past-events/', past_events, name='past_events'),


    #  Category URLs
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('categories/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),

    #  Manage Events (Admin Only)
    path('manage-events/', manage_events, name='manage_events'),

    # Participant 
    path('participant_list/', ParticipantListView.as_view(), name='participant_list'),
    path('participant_create/', ParticipantCreateView.as_view(), name='participant_create'),
    path("participants/delete/<int:pk>/", ParticipantDeleteView.as_view(), name="participant_delete"),




]
