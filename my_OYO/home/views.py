from django.shortcuts import render
from accounts.models import Hotel

# Create your views here.


def index(request):
    hotels = Hotel.objects.all()
    if request.GET.get('search'):
        hotels = hotels.filter(hotel_name_icontains = request.GET.get('search'))

    if request.GET.get('sort_by'):
        sort_by = request.GET.get('sort_by')
        if sort_by == "sort_low":
            hotels = hotels.order_by('hotel_offer_price')
        elif sort_by == "sort_high":
            hotels = hotels.order_by('-hotel_offer_price')
        

    return render(request, 'index.html', context={'hotels':hotels[:50]})



def hotel_details(request, slug):
    hotel = Hotel.objects.get(hotel_slug = slug)
    return render(request, 'hotel_detail.html', context = {'hotel' : hotel})