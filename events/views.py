from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.utils.timezone import now
from django.db.models import Count
from datetime import date
from .models import Event, Category, RSVP, Participant
from .forms import EventForm, CategoryForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, UpdateView, DeleteView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import connection
from django.contrib.auth import get_user_model
from users.decorators import allowed_roles
from django.utils import timezone

User = get_user_model()


# Utility Functions
def is_admin_or_organizer(user):
    return user.groups.filter(name__in=['Admin', 'Organizer']).exists()


# Event Views
class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    login_url = 'login'

    def get_queryset(self):
        queryset = Event.objects.select_related('category').prefetch_related('participants')
        category_id = self.request.GET.get('category')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'category_id': self.request.GET.get('category', ''),
            'start_date': self.request.GET.get('start_date', ''),
            'end_date': self.request.GET.get('end_date', '')
        })
        return context


class CreateEvent(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('event_list')

    def test_func(self):
        return is_admin_or_organizer(self.request.user)


class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('event_list')

    def test_func(self):
        return is_admin_or_organizer(self.request.user)


class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'
    success_url = reverse_lazy('event_list')

    def test_func(self):
        return is_admin_or_organizer(self.request.user)


class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'


@login_required
@allowed_roles(roles=['Admin', 'Organizer'])
def manage_events(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})


# Category Views
class CategoryListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Category
    template_name = 'events/category_list.html'
    context_object_name = 'categories'

    def test_func(self):
        return is_admin_or_organizer(self.request.user)


class CategoryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'events/category_form.html'
    success_url = reverse_lazy('category_list')

    def test_func(self):
        return is_admin_or_organizer(self.request.user)


class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'events/category_form.html'
    success_url = reverse_lazy('category_list')

    def test_func(self):
        return self.request.user.groups.filter(name="Admin").exists()


class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    template_name = 'events/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')

    def test_func(self):
        return self.request.user.groups.filter(name="Admin").exists()


class ParticipantListView(LoginRequiredMixin, ListView):
    model = Participant
    template_name = "events/participant_list.html"
    context_object_name = "participants"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rsvp_events"] = RSVP.objects.filter(user=self.request.user)
        return context

class ParticipantCreateView(CreateView):
    model = Participant
    template_name = "events/participant_form.html"
    fields = ["name", "email"]

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        if Participant.objects.filter(email=email).exists():
            messages.error(self.request, "A participant with this email already exists!")
            return self.form_invalid(form)
        messages.success(self.request, "Participant successfully created!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("participants_list")

class ParticipantDeleteView(DeleteView):
    model = User
    template_name = "events/participant_confirm_delete.html"
    success_url = reverse_lazy("participant_list")

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.kwargs["pk"])


def search_events(request):
    query = request.GET.get('q', '')
    events = Event.objects.filter(name__icontains=query) | Event.objects.filter(location__icontains=query)
    return render(request, 'events/event_list.html', {'events': events, 'query': query})

# RSVP Views
@login_required
def rsvp_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if RSVP.objects.filter(user=request.user, event=event).exists():
        messages.warning(request, "You have already RSVP'd for this event.")
    else:
        RSVP.objects.create(user=request.user, event=event)
        event.participants.add(request.user)
        messages.success(request, f"You have successfully RSVP'd for {event.name}.")

    return redirect('event_detail', event_id=event.id)


@login_required
def cancel_rsvp(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    rsvp = RSVP.objects.filter(user=request.user, event=event).first()

    if rsvp:
        rsvp.delete()
        event.participants.remove(request.user)
        messages.success(request, "Your RSVP has been canceled.")

    return redirect('participant_list')


# Statistics & Filtering Views
def event_stats(request):
    print("event_stats view is being hit")
    return JsonResponse({
        "total_events": Event.objects.count(),
        "total_participants": Participant.objects.count(),  # Use Participant model
        "upcoming_events": Event.objects.filter(date__gte=timezone.now().date()).count(),
        "past_events": Event.objects.filter(date__lt=timezone.now().date()).count()
    })


def filter_events(request, event_type):
    if event_type == "all":
        events = Event.objects.all()  
    elif event_type == "upcoming":
        events = Event.objects.filter(date__gte=date.today())
    elif event_type == "past":
        events = Event.objects.filter(date__lt=date.today())
    else:
        return JsonResponse({"error": "Invalid event type"}, status=400)

    event_list = [{"name": event.name, "date": event.date.strftime("%Y-%m-%d")} for event in events]
    return JsonResponse({"events": event_list})




@login_required
def dashboard(request):
    # Get the total counts in a more optimized way
    total_event = Event.objects.count()
    upcoming_event = Event.objects.filter(date__gte=timezone.now().date()).count()
    past_event = Event.objects.filter(date__lt=timezone.now().date()).count()
    total_participant = Participant.objects.aggregate(total=Count('user'))['total']  
    # Get RSVP events for the user
    user_rsvp_events = request.user.rsvps.values_list('event', flat=True)
    
    # Getting participant count for each event (optimized)
    event_participants = {event.id: event.participants.count() for event in Event.objects.all()}

    counts = {
        'total_events': total_event,
        'upcoming_events': upcoming_event,
        'past_events': past_event,
        'total_participant': total_participant
    }

    context = {
        'user_rsvp_events': Event.objects.filter(id__in=user_rsvp_events),
        'counts': counts,
        'event_participants': event_participants
    }

    return render(request, 'events/dashboard.html', context)

# View for handling AJAX request for total events
def total_events(request):
    events = Event.objects.all().values('name')
    event_list = list(events)
    return JsonResponse({'total_events': event_list})

# View for handling AJAX request for total participants
def total_participants(request):
    participants = Participant.objects.all().values('name', 'email')
    participant_list = list(participants)
    return JsonResponse({'total_participant': participant_list})

# View for handling AJAX request for upcoming events with name and date
def upcoming_events(request):
    upcoming_events = Event.objects.filter(date__gte=timezone.now().date()).values('name', 'date')
    upcoming_event_list = list(upcoming_events)
    return JsonResponse({'upcoming_events': upcoming_event_list})

# View for handling AJAX request for past events
def past_events(request):
    past_events = Event.objects.filter(date__lt=timezone.now().date()).values('name', 'date')
    past_event_list = list(past_events)
    return JsonResponse({'past_events': past_event_list})
