from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Event
from django.urls import reverse
from django.contrib import messages
from .models import Category
def delete_event(request, event_id):
    if request.method == 'POST':
        event= Event.objects.get(id=event_id)
        event.delete()
    return redirect(reverse('cataegory_list'))
def create_event(request):
    if request.method == 'POST':
        # Retrieve data from the POST request
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        priority = request.POST.get('priority')
        description = request.POST.get('description')
        location = request.POST.get('location')
        organizer = request.POST.get('organizer')

        # Retrieve the Category object
        category = Category.objects.get(pk=category_id)

        # Create the Event object
        event = Event.objects.create(
            name=name,
            category=category,
            start_date=start_date,
            end_date=end_date,
            priority=priority,
            description=description,
            location=location,
            organizer=organizer
        )

        # Redirect to the event list page
        return redirect('category_list')
    else:
        categories = Category.objects.all()
        return render(request, 'event_management_system_app/create_event.html', {'categories': categories})
    
def update_event(request , event_id):
    event = Event.objects.get(pk=event_id)
    if request.method == 'POST':
        event.name = request.POST.get('name')
        event.start_date = request.POST.get('start_date')
        event.end_date = request.POST.get('end_date')
        event.priority = request.POST.get('priority')
        event.description = request.POST.get('description')
        event.location = request.POST.get('location')
        event.organizer = request.POST.get('organizer')
        event.allocated_seats = request.POST.get('allocated_seats')
        event.save()
        return redirect('category_list')
    else:
        return render(request,'event_management_system_app/update_event.html', {'event': event})
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'event_management_system_app/category_list.html', {'categories': categories})

def create_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Category.objects.create(name=name)
        return redirect('category_list')
    return render(request, 'event_management_system_app/create_category.html')

def delete_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    if category.event_set.exists():
        messages.error(
            request, "You cannot delete this category as it contains events.")
    else:
        category.delete()
        messages.success(request, "Category deleted successfully.")
    return redirect('category_list')
def category_events(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    events = category.event_set.all()
    return render(request, 'event_management_system_app/category_events.html', {'category': category, 'events': events})
def event_chart(request):
    categories = Category.objects.all()
    pending_counts = {}
    for category in categories:
        pending_counts[category.name] = Event.objects.filter(
            category=category,
            start_date__gt=timezone.now()
        ).count()
    return render(request, 'event_management_system_app/event_chart.html', {'pending_counts': pending_counts})


def usereventlist(request):
    """
    View to display the list of events to the user.
    """
    events = Event.objects.all().order_by('start_date')
    context = {
        'events': events
    }
    return render(request, 'event_management_system_app/user_event_view.html', context)

def event_details(request, event_id):
    """
    View to display detailed information about a specific event.
    """
    event = get_object_or_404(Event, id=event_id)
    context = {
        'event': event
    }
    return render(request, 'event_management_system_app/event_details.html', context)

def register_event(request, event_id):
    """
    View to handle event registration by a user.
    """
    event = get_object_or_404(Event, id=event_id)

    # Example logic to handle registration (adjust as per your requirement)
    if event.allocated_seats > 0:
        event.allocated_seats -= 1
        event.save()
        messages.success(request, f'You have successfully registered for {event.name}.')
    else:
        messages.error(request, 'Sorry, this event is fully booked.')

    return redirect('event_list')
