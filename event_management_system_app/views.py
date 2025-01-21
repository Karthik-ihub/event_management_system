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