from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Event
from django.urls import reverse
def delete_event(request, event_id):
    if request.method == 'POST':
        event= Event.objects.get(id=event_id)
        event.delete()
    return redirect(reverse('cataegory_list'))
def create_event(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Category_id = request.POST.get('category_id')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        priority = request.POST.get('priority')
        description = request.POST.get('description')
        location =  request.POST.get('location')
        organizer = request.POST.get('organizer')

        Category = Category.objects.get(pk=Category_id)
        event = Event(name=name, category=Category, start_date=start_date, end_date=end_date, priority=priority , description=description, location=location, organizer=organizer)
        return redirect('category_list')
    else:
        categories = Category.objects.all()
        return render(request, 'create_event.html', {'categories': categories})
    
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
        event.save()
        return redirect('category_list')
    else:
        return render(request,'event_management_system_app/update_event.html', {'event': event})
