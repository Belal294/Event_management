from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.utils.timezone import now
from django.db.models import Count
from datetime import date
from .models import Event, Category, Participant
from .forms import EventForm, CategoryForm, ParticipantForm
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_roles
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import user_passes_test
from django.db import connection
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import RSVP, Category
from users.views import is_admin
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, UpdateView, DeleteView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test





# Event List View
# @login_required(login_url='login')
# def event_list(request):
#     category_id = request.GET.get('category')
#     start_date = request.GET.get('start_date')
#     end_date = request.GET.get('end_date')
#     events = Event.objects.select_related('category').prefetch_related('participants')

#     if category_id:
#         events = events.filter(category_id=category_id)
#     if start_date and end_date:
#         events = events.filter(date__range=[start_date, end_date])

#     return render(request, 'events/event_list.html', {'events': events})



class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    login_url = 'login'

    def get_queryset(self):
        category_id = self.request.GET.get('category')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        
        queryset = Event.objects.select_related('category').prefetch_related('participants')
        
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_id'] = self.request.GET.get('category', '')
        context['start_date'] = self.request.GET.get('start_date', '')
        context['end_date'] = self.request.GET.get('end_date', '')
        return context





# Event Create View
# @login_required(login_url='login')
# @user_passes_test(is_admin, login_url='no-permission')
# def event_create(request):
#     form = EventForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         connection.close()
        
#         return redirect('event_list')
    
#     return render(request, 'events/event_form.html', {'form': form})

# def is_admin(user):
#     return user.is_authenticated and user.is_staff

# class EventCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
#     model = Event
#     form_class = EventForm
#     template_name = 'events/event_form.html'
#     success_url = reverse_lazy('event_list')
#     login_url = 'login'

#     def test_func(self):
#         return is_admin(self.request.user)

#     def form_valid(self, form):
#         response = super().form_valid(form)
#         connection.close()
#         return response






    
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(user_passes_test(is_admin, login_url='no-permission'), name='dispatch')
class CreateEvent(View):
    def get(self, request, *args, **kwargs):
        form = EventForm()
        return render(request, 'events/event_form.html', {'form': form})
        
        
    def post(self, request, *args, **kwargs):
        form = EventForm(request.POST or None)
        if form.is_valid():
            form.save()
            connection.close()
            return redirect('event_list')
        return render(request, 'events/event_form.html', {'form': form})


class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('event_list')

# Event Update View
# def event_update(request, pk):
#     event = get_object_or_404(Event, pk=pk)
#     form = EventForm(request.POST or None, instance=event)
#     if form.is_valid():
#         form.save()
#         return redirect('event_list')
#     return render(request, 'events/event_form.html', {'form': form})

# Event Delete View
# def event_delete(request, pk):
#     event = get_object_or_404(Event, pk=pk)
#     if request.method == "POST":
#         event.delete()
#         return redirect('event_list')
#     return render(request, 'events/event_confirm_delete.html', {'event': event})

class EventDeleteView(DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'
    success_url = reverse_lazy('event_list')


# # Event Detail View
# def event_detail(request, pk):
#     event = get_object_or_404(Event, pk=pk)
#     return render(request, 'events/event_detail.html', {'event': event})


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'


def filter_events(request, event_type):
    filters = {
        "upcoming": Event.objects.filter(date__gte=date.today()),
        "past": Event.objects.filter(date__lt=date.today())
    }
    events = filters.get(event_type, Event.objects.all())
    event_list = [{"name": event.name, "date": event.date.strftime("%Y-%m-%d")} for event in events]
    return JsonResponse({"events": event_list})

# Dashboard View
def dashboard(request):
    return render(request, 'events/dashboard.html', {
        'total_events': Event.objects.count(),
        'upcoming_events': Event.objects.filter(date__gte=now().date()).count(),
        'past_events': Event.objects.filter(date__lt=now().date()).count(),
        'todays_events': Event.objects.filter(date=now().date()),
    })



def event_statistics(request):
    return JsonResponse({
        "total_events": Event.objects.count(),
        "total_participants": Participant.objects.count()
    })




# Category CRUD
# @login_required(login_url='login')
# @user_passes_test(is_admin, login_url='no-permission')
# def category_list(request):
#     return render(request, 'events/category_list.html', {'categories': Category.objects.all()})

# def category_create(request):
#     form = CategoryForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         return redirect('category_list')
#     return render(request, 'events/category_form.html', {'form': form})

# def category_update(request, pk):
#     category = get_object_or_404(Category, pk=pk)
#     form = CategoryForm(request.POST or None, instance=category)
#     if form.is_valid():
#         form.save()
#         return redirect('category_list')
#     return render(request, 'events/category_form.html', {'form': form})

# def category_delete(request, pk):
#     category = get_object_or_404(Category, pk=pk)
#     if request.method == "POST":
#         category.delete()
#         return redirect('category_list')
#     return render(request, 'events/category_confirm_delete.html', {'category': category})


def is_admin(user):
    return user.is_authenticated and user.groups.filter(name="Admin").exists()

class AdminRequiredMixin(View):
   

    @method_decorator(login_required(login_url='login'), name='dispatch')
    @method_decorator(user_passes_test(is_admin, login_url='no-permission'), name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CategoryListView(AdminRequiredMixin, ListView):
    model = Category
    template_name = 'events/category_list.html'
    context_object_name = 'categories'

class CategoryCreateView(AdminRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'events/category_form.html'
    success_url = reverse_lazy('category_list')

class CategoryUpdateView(AdminRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'events/category_form.html'
    success_url = reverse_lazy('category_list')

class CategoryDeleteView(AdminRequiredMixin, DeleteView):
    model = Category
    template_name = 'events/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')




def event_stats(request):
    total_events = Event.objects.count()
    total_participants = Participant.objects.count()
    upcoming_events = Event.objects.filter(date__gte=date.today()).count()
    past_events = Event.objects.filter(date__lt=date.today()).count()
    
    return JsonResponse({
        "total_events": total_events,
        "total_participants": total_participants,
        "upcoming_events": upcoming_events,
        "past_events": past_events
    })


def filter_events(request, event_type):
    if event_type == "upcoming":
        events = Event.objects.filter(date__gte=date.today())
    elif event_type == "past":
        events = Event.objects.filter(date__lt=date.today())
    else:  
        events = Event.objects.all()

    event_list = [{"name": event.name, "date": event.date.strftime("%Y-%m-%d")} for event in events]
    return JsonResponse({"events": event_list})




# @login_required
# def participant_list(request):
#     rsvp_events = RSVP.objects.filter(user=request.user)
#     participants = Participant.objects.all()
#     return render(request, "events/participant_list.html", {"participants": participants})
#     # events = Event.objects.filter(participants=request.user)
#     # participants = User.objects.filter(events_participated__in=events).distinct()
#     # return render(request, 'events/participant_list.html', {
#     #     'rsvp_events': rsvp_events,
#     #     'participants': participants,

#     # })




# def participant_create(request):
#     if request.method == "POST":
#         name = request.POST.get("name", "").strip()  
#         email = request.POST.get("email", "").strip()

#         if not name or not email:
#             messages.error(request, "Name and Email are required!")
#         elif Participant.objects.filter(email=email).exists():
#             messages.error(request, "A participant with this email already exists!")
#         else:
#             Participant.objects.create(name=name, email=email)
#             messages.success(request, "Participant successfully created!")
#             return redirect("participants_list")

#     return render(request, "events/participant_form.html")


# def participant_delete(request, pk):
#     user = get_object_or_404(User, pk=pk)
#     if request.method == "POST":
#         user.delete()
#         return redirect('participant_list')
#     return render(request, 'events/participant_confirm_delete.html', {'user': user})


def search_events(request):
    query = request.GET.get('q', '')
    events = Event.objects.filter(name__icontains=query) | Event.objects.filter(location__icontains=query)
    return render(request, 'events/event_list.html', {'events': events, 'query': query})

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





def is_admin(user):
    return user.is_superuser  

@user_passes_test(is_admin)
def manage_events(request):
    events = Event.objects.all()  
    return render(request, 'events/event_list.html', {'events': events})




@login_required
def rsvp_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Check if the user has already RSVP'd
    if RSVP.objects.filter(user=request.user, event=event).exists():
        messages.warning(request, "You have already RSVP'd for this event.")
        return redirect('event_detail', event_id=event.id)

    # Save RSVP
    RSVP.objects.create(user=request.user, event=event)
    event.participants.add(request.user)
    messages.success(request, f"You have successfully RSVP'd for {event.name}.")

    # Send Confirmation Email
    # send_mail(
    #     subject="Event RSVP Confirmation",
    #     message=f"Dear {request.user.username},\n\nYou have successfully RSVP'd for {event.name} on {event.date} at {event.time}.\n\nThank you!",
    #     from_email="noreply@example.com",
    #     recipient_list=[request.user.email],
    #     fail_silently=True,
    # )

    return redirect('event_detail', event_id=event.id)




@login_required
def participant_dashboard(request):
    rsvp_events = request.user.rsvps.all()
    print(rsvp_event)
    return render(request, 'events/participant_list.html', {'rsvp_events': rsvp_events})





@login_required
def cancel_rsvp(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    rsvp = RSVP.objects.filter(user=request.user, event=event).first()

    if rsvp:
        rsvp.delete()
        event.participants.remove(request.user)  
        messages.success(request, "Your RSVP has been canceled.")

    return redirect('participant_list')  

