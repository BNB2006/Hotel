from django.db import models
from django.contrib.auth.models import User

class HotelUser(User):
    profile_picture = models.ImageField(upload_to="profile")
    phone_number =  models.CharField(unique = True , max_length= 100)
    email_token = models.CharField(max_length = 225 ,null = True , blank=True)
    otp = models.CharField(max_length = 10 , null = True , blank = True)
    is_verified = models.BooleanField(default = False)

    class Meta:
        db_table = "hotel_user"


class HotelVendor(User):
    phone_number =  models.CharField(unique = True, max_length= 100)
    business_name = models.CharField(max_length=100, null=True, blank=True)
    profile_picture = models.ImageField(upload_to="profile")
    email_token = models.CharField(max_length = 225 ,null = True , blank=True)
    otp = models.CharField(max_length = 10 , null = True , blank = True)
    is_verified = models.BooleanField(default = False)

    class Meta:
        db_table = "hotel_vendor"


class Ameneties(models.Model):
    name = models.CharField(max_length = 1000)
    icon = models.ImageField(upload_to="hotels", null=True)

    def __str__(self) -> str: #return a string representation of the amenity name.
        return self.name

class Hotel(models.Model):
    hotel_name  = models.CharField(max_length = 100)
    hotel_description = models.TextField()
    hotel_slug = models.SlugField(max_length = 225 , unique  = True)
    hotel_owner = models.ForeignKey(HotelVendor, on_delete = models.CASCADE , related_name = "hotels")
    ameneties = models.ManyToManyField(Ameneties)
    hotel_price = models.FloatField()
    hotel_offer_price = models.FloatField()
    hotel_location = models.TextField()
    is_active = models.BooleanField(default = True)


class HotelImages(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete = models.CASCADE , related_name = "hotel_images")
    image = models.ImageField(upload_to="hotels")

class HotelManager(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete = models.CASCADE , related_name = "hotel_managers")
    manager_name = models.CharField(max_length = 100)
    manager_contact = models.CharField(max_length = 100)

