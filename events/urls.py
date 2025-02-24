from django.urls import path
from django.contrib.auth import views as auth_views
from events.views import (
    filter_events, dashboard, event_statistics, event_stats,
    search_events, manage_events, rsvp_event,cancel_rsvp, EventListView, CreateEvent, EventUpdateView, EventDeleteView, EventDetailView, CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView, ParticipantListView, ParticipantCreateView, ParticipantDeleteView
)
from users.views import sign_up, sign_in, sign_out, signup_view, admin_dashboard


urlpatterns = [
    # Authentication
    path('sign-up/', sign_up, name='sign-up'),
    path('login/', sign_in, name='login'),
    path('logout/', sign_out, name='logout'),
    path("signup/", signup_view, name="signup"),

    # Dashboard
    path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('dashboard/', dashboard, name='dashboard'),

    # Event URLs
    # path('events/', event_list, name='event_list'),
    # path('events/create/', event_create, name='event_create'),
    path('events/create/', CreateEvent.as_view(), name='event_create'),
    path('events/', EventListView.as_view(), name='event_list'),
    # path('events/create/', EventCreateView.as_view(), name='event_create'),
    path('event/update/<int:pk>/', EventUpdateView.as_view(), name='event_update'),


    # path('events/<int:pk>/update/', event_update, name='event_update'),

    # path('events/<int:pk>/delete/', event_delete, name='event_delete'),
    path('event/delete/<int:pk>/', EventDeleteView.as_view(), name='event_delete'),
    # path('events/<int:pk>/', event_detail, name='event_detail'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event_detail'),

    path('events/filter/<str:event_type>/', filter_events, name='filter_events'),

    # Event Statistics
    path('events/statistics/', event_statistics, name='event_statistics'),
    path('events/stats/', event_stats, name='event_stats'),

    # Category URLs
    # path('categories/', category_list, name='category_list'),
    # path('categories/create/', category_create, name='category_create'),
    # path('categories/<int:pk>/update/', category_update, name='category_update'),
    # path('categories/<int:pk>/delete/', category_delete, name='category_delete'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('categories/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),


    # Participant Management (Admin Only)
    # path('participants/', participant_list, name='participant_list'),
    # path("participants/create/", participant_create, name="participant_create"),
    # path('participants/<int:pk>/delete/', participant_delete, name='participant_delete'),
    path("participants/", ParticipantListView.as_view(), name="participant_list"),
    path("participants/create/", ParticipantCreateView.as_view(), name="participant_create"),
    path("participants/delete/<int:pk>/", ParticipantDeleteView.as_view(), name="participant_delete"),



    # Search Events
    path('search/', search_events, name='search_events'),

    # Manage Events (Admin Only)
    path('manage-events/', manage_events, name='manage_events'),

    # Django Auth Views (For built-in login/logout)
    path("auth-login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="auth-login"),
    path("auth-logout/", auth_views.LogoutView.as_view(), name="auth-logout"),

    path('event/<int:event_id>/rsvp/', rsvp_event, name='rsvp_event'),
    path('event/<int:event_id>/cancel_rsvp/', cancel_rsvp, name='cancel_rsvp'),

]

