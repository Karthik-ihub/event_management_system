from django.http import HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from event_management_system_app.forms import ChangePasswordForm, CustomerProfile, LoginForm, RegistrationForm
from .models import Category, Event , Customer
from django.shortcuts import render, redirect
from django.urls import reverse

# Registration Function
def user_Regi(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, 'Registration Successful!')
      return HttpResponseRedirect('/login')
  else:
    form = RegistrationForm()
  return render(request, 'event_management_system_app/registration.html', {'form':form})
      
# Login Function
def user_Login(request):
  if request.user.is_authenticated:
    return HttpResponseRedirect('/')
  else:
    if request.method == 'POST':
      form = LoginForm(request=request, data=request.POST)
      if form.is_valid():
        uname = form.cleaned_data.get('username')
        upass = form.cleaned_data.get('password')
        validUser = authenticate(username=uname, password=upass)
        if validUser is not None:
          login(request, validUser)
          return HttpResponseRedirect('/')
          messages.success(request, 'Login Successful!')
    else:
      form = LoginForm()
  return render (request, 'event_management_system_app/login.html', {'form': form})
  
# User logout
def user_Logout(request):
  logout(request)
  return HttpResponseRedirect('/login')
  
 
# Profile Function
def user_Profile(request):
  if request.method == 'POST':
    usr = request.user
    print(usr)
    form = CustomerProfile(request.POST)
    if form.is_valid():
      name = form.cleaned_data.get('name')
      locality = form.cleaned_data.get('locality')
      city = form.cleaned_data.get('city')
      state = form.cleaned_data.get('state')
      zipcode = form.cleaned_data.get('zipcode')
      cust = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode = zipcode)
      cust.save()
      messages.success(request, 'Profile Set Successful!')
      return HttpResponseRedirect('/address')
  else:
    form = CustomerProfile()
  return render(request, 'myapp/profile.html', {'form': form})

#Change Password Function
def change_Password(request):
  if request.method == 'POST':
    form = ChangePasswordForm(user=request.user, data=request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, 'Password Has Been Changed Successful!')
      return HttpResponseRedirect('/login')
  else:
    form = ChangePasswordForm(request.user)
  return render(request, 'event_management_system_app/changepassword.html', {'form':form})

def delete_event(request, event_id):
    if request.method == 'POST':
        event = Event.objects.get(id=event_id)
        event.delete()
    return redirect(reverse('category_list'))


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


def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.method == 'POST':
        # Update event fields based on form data
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
        # Render update event page with event data
        return render(request, 'event_management_system_app/update_event.html', {'event': event})

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
