from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Participant, Category
from .forms import EventForm, ParticipantForm, CategoryForm
from django.db.models import Count
from django.utils.timezone import now
from django.http import JsonResponse
from datetime import datetime


def event_list(request):
    category_id = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    events = Event.objects.select_related('category').prefetch_related('participants')

    if category_id:
        events = events.filter(category_id=category_id)

    if start_date and end_date:
        events = events.filter(date__range=[start_date, end_date])

    total_participants = Event.objects.aggregate(total=Count('participants'))['total']

    return render(request, 'events/event_list.html', {
        'events': events,
        'total_participants': total_participants
    })


def event_create(request):
   if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')  
   else:
        form = EventForm()
    
   return render(request, 'events/event_form.html', {'form': form})
        

def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')  
    else:
        form = EventForm(instance=event)
    
    return render(request, 'events/event_form.html', {'form': form})


def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        event.delete()
        return redirect('event_list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})

def dashboard(request):
    total_participants = Participant.objects.count()
    total_events = Event.objects.count()
    upcoming_events = Event.objects.filter(date__gte=now().date()).count()
    past_events = Event.objects.filter(date__lt=now().date()).count()
    todays_events = Event.objects.filter(date=now().date())


    context = {
        'total_participants': total_participants,
        'total_events': total_events,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'todays_events': todays_events,
    }

    return render(request, 'events/dashboard.html', context)



def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})



def filter_events(request, event_type):
    if event_type == "upcoming":
        events = Event.objects.filter(date__gte=now()).order_by("date")  
    elif event_type == "past":
        events = Event.objects.filter(date__lt=now()).order_by("-date")  
    else:
        return JsonResponse({"error": "Invalid event type"}, status=400)

    event_list = [{"name": event.name, "date": event.date.strftime("%Y-%m-%d")} for event in events]
    return JsonResponse({"events": event_list})


def upcoming_events(request):
    today = datetime.today().date()
    events = Event.objects.filter(date__gte=today) 
    return render(request, 'events/upcoming_events.html', {'events': events})



def search_events(request):
    query = request.GET.get('q', '')  
    events = Event.objects.filter(
        name__icontains=query 
    ) | Event.objects.filter(
        location__icontains=query  
    )

    return render(request, 'events/event_list.html', {'events': events, 'query': query})



