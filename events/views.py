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

# Event List View
@login_required(login_url='login')
def event_list(request):
    category_id = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    events = Event.objects.select_related('category').prefetch_related('participants')

    if category_id:
        events = events.filter(category_id=category_id)
    if start_date and end_date:
        events = events.filter(date__range=[start_date, end_date])

    return render(request, 'events/event_list.html', {'events': events})

# Event Create View
@login_required(login_url='login')
@allowed_roles(['Organizer', 'Admin'])
def event_create(request):
    form = EventForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('event_list')
    return render(request, 'events/event_form.html', {'form': form})
# Event Update View
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('event_list')
    return render(request, 'events/event_form.html', {'form': form})

# Event Delete View
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        event.delete()
        return redirect('event_list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})


# Event Detail View
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})

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
@login_required(login_url='login')
@allowed_roles(['Organizer', 'Admin'])
def category_list(request):
    return render(request, 'events/category_list.html', {'categories': Category.objects.all()})

@allowed_roles(['Organizer', 'Admin'])
def category_create(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('category_list')
    return render(request, 'events/category_form.html', {'form': form})

@allowed_roles(['Organizer', 'Admin'])
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect('category_list')
    return render(request, 'events/category_form.html', {'form': form})

@allowed_roles(['Organizer', 'Admin'])
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        return redirect('category_list')
    return render(request, 'events/category_confirm_delete.html', {'category': category})





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



# Participant Management (Admin Only)
@allowed_roles(['Admin'])
def participant_list(request):
    participants = User.objects.filter(groups__name="Participant")
    return render(request, 'participants/participant_list.html', {'participants': participants})

@allowed_roles(['Admin'])
def participant_create(request):
    form = ParticipantForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()
        participant_group = Group.objects.get(name="Participant")
        user.groups.add(participant_group)
        return redirect('participant_list')
    return render(request, 'participants/participant_form.html', {'form': form})

@allowed_roles(['Admin'])
def participant_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        user.delete()
        return redirect('participant_list')
    return render(request, 'participants/participant_confirm_delete.html', {'user': user})


def search_events(request):
    query = request.GET.get('q', '')
    events = Event.objects.filter(name__icontains=query) | Event.objects.filter(location__icontains=query)
    return render(request, 'events/event_list.html', {'events': events, 'query': query})


def is_admin(user):
    return user.is_superuser  

@user_passes_test(is_admin)
def manage_events(request):
    events = Event.objects.all()  
    return render(request, 'events/event_list.html', {'events': events})

