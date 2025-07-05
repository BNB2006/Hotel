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
        return redirect('/')  # or your user login URL name
    print('user:',request.user)
    hotels = Hotel.objects.all()
    if request.GET.get('search'):
        hotels = hotels.filter(hotel_name_icontains = request.GET.get('search'))

    if request.GET.get('sort_by'):
        sort_by = request.GET.get('sort_by')
        if sort_by == "sort_low":
            hotels = hotels.order_by('hotel_offer_price')
        elif sort_by == "sort_high":
            hotels = hotels.order_by('-hotel_offer_price')
        

    messages.success(request,"Welocme")
    return render(request, 'index.html', context={'hotels':hotels[:50]})



def hotel_details(request, slug):
    hotel = Hotel.objects.get(hotel_slug = slug)
    return render(request, 'hotel_detail.html', context = {'hotel' : hotel})


def hotel_details(request, slug):
    hotel = Hotel.objects.get(hotel_slug = slug)

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
            hotel = hotel,
            booking_user = HotelUser.objects.get(id = request.user.id),
            booking_start_date = start_date,
            booking_end_date =end_date,
            price = hotel.hotel_offer_price * days_count
        )
        messages.success(request, "Booking Captured.")

        return HttpResponseRedirect(request.path_info)


    return render(request, 'hotel_detail.html', context = {'hotel' : hotel})