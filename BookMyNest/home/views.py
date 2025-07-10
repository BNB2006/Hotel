from django.shortcuts import render, redirect
from .models import HotelBooking
from accounts.models import Hotel, HotelUser, HotelVendor
from django.http import HttpResponseRedirect
from django.contrib import messages
import datetime
from django.contrib.auth import logout

# Create your views here.


def index(request):
    # If vendor, log out and redirect to login page
    if request.user.is_authenticated and hasattr(request.user, 'hotelvendor'):
        messages.error(request,"Please login as user!")
        logout(request)
        return redirect('/')
    
    print('user:',request.user)
    # Show only 4 featured hotels on landing page
    hotels = Hotel.objects.all()[:4]
    return render(request, 'index.html', context={'hotels': hotels})


def hotels(request):
    # If vendor, log out and redirect to login page
    if request.user.is_authenticated and hasattr(request.user, 'hotelvendor'):
        messages.error(request,"Please login as user!")
        logout(request)
        return redirect('/')
    
    hotels = Hotel.objects.all()
    
    # Get search and sort parameters
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort_by', '')
    
    # Apply search filter
    if search_query:
        hotels = hotels.filter(hotel_name__icontains=search_query)

    # Apply sorting
    if sort_by == "sort_low":
        hotels = hotels.order_by('hotel_offer_price')
    elif sort_by == "sort_high":
        hotels = hotels.order_by('-hotel_offer_price')
        

    return render(request, 'hotels.html', context={
        'hotels': hotels,
        'search_query': search_query,
        'sort_by': sort_by
    })


def hotel_details(request, slug):
    hotel = Hotel.objects.get(hotel_slug=slug)

    if request.method == "POST":
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        days_count = (end_date - start_date).days

        if days_count <= 0:
            messages.warning(request, "Invalid Booking Date.")
            return HttpResponseRedirect(request.path_info)

        HotelBooking.objects.create(
            hotel=hotel,
            booking_user=HotelUser.objects.get(id=request.user.id),
            booking_start_date=start_date,
            booking_end_date=end_date,
            price=hotel.hotel_offer_price * days_count
        )
        messages.success(request, "Booking Captured.")
        return HttpResponseRedirect(request.path_info)

    return render(request, 'hotel_detail.html', context={'hotel': hotel})