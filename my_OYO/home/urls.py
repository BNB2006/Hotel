from django.urls import path, include
from home import views

urlpatterns = [
    path('' , views.index , name="index"),
    path('hotels/', views.hotels, name="hotels"),
    path('hotel-details/<slug>/', views.hotel_details, name="hotel_details")
]


