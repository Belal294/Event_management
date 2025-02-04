from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.utils.timezone import now
from django.db.models import Count
from datetime import date
from .models import Event, Participant, Category
from .forms import EventForm, CategoryForm

def event_list(request):
    category_id = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    events = Event.objects.select_related('category').prefetch_related('participants')

    if category_id:
        events = events.filter(category_id=category_id)
    if start_date and end_date:
        events = events.filter(date__range=[start_date, end_date])

    return render(request, 'events/event_list.html', {
        'events': events,
        'total_participants': Participant.objects.count()
    })

def event_create(request):
    form = EventForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('event_list')
    return render(request, 'events/event_form.html', {'form': form})

def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('event_list')
    return render(request, 'events/event_form.html', {'form': form})

def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        event.delete()
        return redirect('event_list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})

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

def dashboard(request):
    return render(request, 'events/dashboard.html', {
        'total_participants': Participant.objects.count(),
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

def search_events(request):
    query = request.GET.get('q', '')
    events = Event.objects.filter(name__icontains=query) | Event.objects.filter(location__icontains=query)
    return render(request, 'events/event_list.html', {'events': events, 'query': query})

def category_list(request):
    return render(request, 'events/category_list.html', {'categories': Category.objects.all()})

def category_create(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('category_list')
    return render(request, 'events/category_form.html', {'form': form})

def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect('category_list')
    return render(request, 'events/category_form.html', {'form': form})

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

