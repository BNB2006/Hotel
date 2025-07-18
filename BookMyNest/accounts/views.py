from django.shortcuts import render, redirect, HttpResponse
from .models import HotelUser, HotelVendor, Hotel, Ameneties, HotelImages
from home.models import HotelBooking
from django.db.models import Q
from django.contrib import messages
from .utils import generateRandomToken, sendEmailToken, sendOTPtoEmail , generateSlug
from django.contrib.auth import authenticate, login, logout
import random
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseForbidden
from django.contrib.auth.models import User

# Create your views here.
def login_page(request):    
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        hotel_user = HotelUser.objects.filter(
            email = email)


        if not hotel_user.exists():
            messages.warning(request, "No Account Found.")
            return redirect('/accounts/login/')

        if not hotel_user[0].is_verified:
            messages.warning(request, "Account not verified")
            return redirect('/accounts/login/')

        hotel_user = authenticate(username = hotel_user[0].username , password=password)

        if hotel_user:
            messages.success(request, "Login Success")
            login(request , hotel_user)
            return redirect('/')

        messages.warning(request, "Invalid credentials")
        return redirect('/accounts/login/')
    return render(request, 'login.html')


def register(request):
    if request.method == "POST":

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        username = request.POST.get('username')

        # Check if username already exists
        if HotelUser.objects.filter(username=username).exists() or User.objects.filter(username=username).exists():
            messages.warning(request, "Username is already taken.")
            return redirect('/accounts/register/')

        hotel_user = HotelUser.objects.filter(
            Q(email = email) | Q(phone_number  = phone_number)
        )

        if hotel_user.exists():
            messages.warning(request, "Account exists with Email or Phone Number.")
            return redirect('/accounts/register/')

        hotel_user = HotelUser.objects.create(
            username = username,
            first_name = first_name,
            last_name = last_name,
            email = email,
            phone_number = phone_number,
            email_token = generateRandomToken()
        )
        hotel_user.set_password(password)
        hotel_user.save()

        sendEmailToken(request, email , hotel_user.email_token, "user")

        messages.success(request, "An email Sent to your Email")
        return redirect('/accounts/register/')


    return render(request, 'register.html')


#Email verification for user
def verify_email_token(request, token):
    try:
        hotel_user = HotelUser.objects.get(email_token=token)
        hotel_user.is_verified = True
        hotel_user.save()
        messages.success(request, "Email verified")
        return redirect('/accounts/login/')
    except HotelUser.DoesNotExist:
        return HttpResponse("Invalid Token")

# #emial verification for vendor
def verify_email_token_vendor(request, token):
    try:
        hotel_user = HotelVendor.objects.get(email_token=token)
        hotel_user.is_verified = True
        hotel_user.save()
        messages.success(request, "Email verified")
        return redirect('/accounts/login-vendor/')
    except HotelUser.DoesNotExist:
        return HttpResponse("Invalid Token")
    

def send_otp_page(request):
    return render(request, 'verify_otp.html')

def ajax_send_otp(request):
    if request.method == "POST":
        email = request.POST.get('email')
        hotel_user = HotelUser.objects.filter(email=email)
        if not hotel_user.exists():
            return JsonResponse({'success': False, 'message': 'No Account Found.'})
        otp = random.randint(1000, 9999)
        hotel_user.update(otp=otp)
        sendOTPtoEmail(email, otp)
        # Store email in session for verification step
        request.session['otp_email'] = email
        return JsonResponse({'success': True, 'message': 'OTP sent to your email.'})
    return JsonResponse({'success': False, 'message': 'Invalid request.'})

def verify_otp(request):
    if request.method == "POST":
        otp = request.POST.get('otp')
        email = request.session.get('otp_email')
        if not email:
            messages.warning(request, "Session expired. Please try again.")
            return redirect('login_page')
        try:
            hotel_user = HotelUser.objects.get(email=email)
        except HotelUser.DoesNotExist:
            messages.warning(request, "No Account Found.")
            return redirect('login_page')
        if otp == str(hotel_user.otp):
            login(request, hotel_user)
            messages.success(request, "Login Success")
            # Remove email from session
            request.session.pop('otp_email', None)
            return redirect('/')
        else:
            messages.warning(request, "Wrong OTP")
            return render(request, 'verify_otp.html')
    return render(request, 'verify_otp.html')

def login_vendor(request):    
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        hotel_user = HotelVendor.objects.filter(
            email = email)


        if not hotel_user.exists():
            messages.warning(request, "No Account Found.")
            return redirect('/accounts/login-vendor/')

        if not hotel_user[0].is_verified:
            messages.warning(request, "Account not verified")
            return redirect('/accounts/login-vendor/')

        hotel_user = authenticate(username = hotel_user[0].username , password=password)

        if hotel_user:
            login(request , hotel_user)
            return redirect('/accounts/dashboard/')

        messages.warning(request, "Invalid credentials")
        return redirect('/accounts/login-vendor/')
    
    return render(request, 'vendor/login_vendor.html')


def register_vendor(request):
    if request.method == "POST":

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        business_name = request.POST.get('business_name')

        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        username = request.POST.get('username')

        # Check if username already exists
        if HotelVendor.objects.filter(username=username).exists() or User.objects.filter(username=username).exists():
            messages.warning(request, "Username is already taken.")
            return redirect('/accounts/register-vendor/')

        hotel_user = HotelVendor.objects.filter(
            Q(email = email) | Q(phone_number  = phone_number)
        )

        if hotel_user.exists():
            messages.warning(request, "Account exists with Email or Phone Number.")
            return redirect('/accounts/register-vendor/')

        hotel_user = HotelVendor.objects.create(
            username = username,
            first_name = first_name,
            last_name = last_name,
            email = email,
            phone_number = phone_number,
            business_name = business_name,
            email_token = generateRandomToken()
        )
        hotel_user.set_password(password)
        hotel_user.save()

        sendEmailToken(request, email , hotel_user.email_token, "vendor")

        messages.success(request, "An email Sent to your Email")
        return redirect('/accounts/register-vendor/')


    return render(request, 'vendor/register_vendor.html')


@login_required(login_url='login_vendor')
def dashboard(request):
    if not hasattr(request.user, 'hotelvendor'):
        messages.error(request,"Please login as Vendor!")
        logout(request)
        return redirect('/accounts/login-vendor')
    hotels = Hotel.objects.filter(hotel_owner = request.user)
    vendor = request.user.hotelvendor
    context = {'hotels': hotels, 'vendor': vendor}
    return render(request, 'vendor/vendor_dashboard.html', context)


@login_required(login_url='login_vendor')
def add_hotel(request):
    if request.method == "POST":
        hotel_name = request.POST.get('hotel_name')
        hotel_description = request.POST.get('hotel_description')
        ameneties= request.POST.getlist('ameneties[]')
        hotel_price= request.POST.get('hotel_price')
        hotel_offer_price= request.POST.get('hotel_offer_price')
        hotel_location= request.POST.get('hotel_location')
        hotel_slug = generateSlug(hotel_name)

        hotel_vendor = HotelVendor.objects.get(id = request.user.id)

        hotel_obj = Hotel.objects.create(
            hotel_name = hotel_name,
            hotel_description = hotel_description,
            hotel_price = hotel_price,
            hotel_offer_price = hotel_offer_price,
            hotel_location = hotel_location,
            hotel_slug = hotel_slug,
            hotel_owner = hotel_vendor 
        )
        
        for ameneti in ameneties:
            ameneti = Ameneties.objects.get(id = ameneti)
            hotel_obj.ameneties.add(ameneti)
            hotel_obj.save()

        messages.success(request, "Hotel Created")
        return redirect('/accounts/dashboard/')


    ameneties = Ameneties.objects.all()
    vendor = request.user.hotelvendor
    return render(request, 'vendor/add_hotel.html', context={'ameneties': ameneties, 'vendor': vendor})

@login_required(login_url='login_vendor')
def delete_hotel(request, slug):
    hotel_obj = Hotel.objects.get(hotel_slug = slug)
    hotel_obj.delete()
    messages.success(request, "Hotel Deleted.")
    return redirect('/accounts/dashboard/')

@login_required(login_url='login_vendor')
def upload_images(request, slug):
    hotel_obj = Hotel.objects.get(hotel_slug = slug)
    vendor = request.user.hotelvendor
    if request.method == "POST":
        image = request.FILES['image']
        HotelImages.objects.create(
        hotel = hotel_obj,
        image = image
        )
        messages.success(request, "image uploaded succesfully")
        return HttpResponseRedirect(request.path_info)

    return render(request, 'vendor/upload_images.html', context = {'images' : hotel_obj.hotel_images.all(), 'vendor': vendor})

@login_required(login_url='login_vendor')
def delete_image(request, id):
    hotel_image = HotelImages.objects.get(id = id)
    hotel_image.delete()
    messages.warning(request, "Hotel Image deleted")
    return redirect('/accounts/dashboard/')


@login_required(login_url='login_vendor')
def edit_hotel(request, slug):
    hotel_obj = Hotel.objects.get(hotel_slug=slug)
    
    # Check if the current user is the owner of the hotel
    if request.user.id != hotel_obj.hotel_owner.id:
        return HttpResponse("You are not authorized")

    if request.method == "POST":
        # Retrieve updated hotel details from the form
        hotel_name = request.POST.get('hotel_name')
        hotel_description = request.POST.get('hotel_description')
        ameneties= request.POST.getlist('ameneties[]')
        hotel_price = request.POST.get('hotel_price')
        hotel_offer_price = request.POST.get('hotel_offer_price')
        hotel_location = request.POST.get('hotel_location')
        
        # Update hotel object with new details
        hotel_obj.hotel_name = hotel_name
        hotel_obj.hotel_description = hotel_description
        hotel_obj.hotel_price = hotel_price
        hotel_obj.hotel_offer_price = hotel_offer_price
        hotel_obj.hotel_location = hotel_location

        for ameneti in ameneties:
            ameneti = Ameneties.objects.get(id = ameneti)
            hotel_obj.ameneties.add(ameneti)
            hotel_obj.save()
        hotel_obj.save()
        
        messages.success(request, "Hotel Details Updated")

        return HttpResponseRedirect(request.path_info)

    # Retrieve amenities for rendering in the template
    ameneties = Ameneties.objects.all()
    vendor = request.user.hotelvendor
    # Render the edit_hotel.html template with hotel and amenities as context
    return render(request, 'vendor/edit_hotel.html', context={'hotel': hotel_obj, 'ameneties': ameneties, 'vendor': vendor})

@login_required(login_url='login_vendor')
def bookings(request):
    # Only allow HotelVendor users
    if not hasattr(request.user, 'hotelvendor') and not isinstance(request.user, HotelVendor):
        return HttpResponseForbidden("You are not authorized to view this page.")
    hotels = Hotel.objects.filter(hotel_owner=request.user)
    bookings = HotelBooking.objects.filter(hotel__in=hotels).select_related('hotel', 'booking_user')
    vendor = request.user.hotelvendor
    return render(request, "vendor/bookings.html", {"bookings": bookings, 'vendor': vendor})

def logout_vendor(request):
    logout(request)
    messages.success(request, "Logout Success")
    return redirect('/accounts/login-vendor/')

@login_required(login_url='login_vendor')
def vendor_settings(request):
    # Only allow HotelVendor users
    if not hasattr(request.user, 'hotelvendor') and not isinstance(request.user, HotelVendor):
        return HttpResponseForbidden("You are not authorized to view this page.")
    
    vendor = request.user.hotelvendor if hasattr(request.user, 'hotelvendor') else request.user
    
    if request.method == "POST":
        # Handle profile update
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        business_name = request.POST.get('business_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        
        # Check if username is already taken by another user
        if username != vendor.username:
            existing_user = HotelVendor.objects.filter(username=username).exclude(id=vendor.id)
            if existing_user.exists():
                messages.error(request, "Username is already taken by another user.")
                return redirect('vendor_settings')
        # Check if email is already taken by another user
        if email != vendor.email:
            existing_user = HotelVendor.objects.filter(email=email).exclude(id=vendor.id)
            if existing_user.exists():
                messages.error(request, "Email is already taken by another user.")
                return redirect('vendor_settings')
        # Check if phone number is already taken by another user
        if phone_number != vendor.phone_number:
            existing_user = HotelVendor.objects.filter(phone_number=phone_number).exclude(id=vendor.id)
            if existing_user.exists():
                messages.error(request, "Phone number is already taken by another user.")
                return redirect('vendor_settings')
        # Update user information
        vendor.username = username
        vendor.first_name = first_name
        vendor.last_name = last_name
        vendor.business_name = business_name
        vendor.email = email
        vendor.phone_number = phone_number
        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            vendor.profile_picture = request.FILES['profile_picture']
        vendor.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('vendor_settings')
    
    return render(request, 'vendor/settings.html', {'vendor': vendor})

def logout_user(request):
    logout(request)
    messages.success(request, "Logout Success")
    return redirect('/')

@login_required(login_url='login_page')
def user_profile(request):
    # Only allow HotelUser users
    if not hasattr(request.user, 'hoteluser'):
        return HttpResponseForbidden("You are not authorized to view this page.")
    user = request.user
    hoteluser = user.hoteluser
    from django.http import JsonResponse
    from home.models import HotelBooking  # <-- add this import for bookings
    # Fetch bookings for this user
    bookings = HotelBooking.objects.filter(booking_user=hoteluser).select_related('hotel').order_by('-booking_start_date')
    if request.method == "POST":
        # Handle AJAX profile picture upload
        if request.FILES.get('profile_picture') and request.POST.get('ajax') == '1':
            profile_picture = request.FILES['profile_picture']
            hoteluser.profile_picture = profile_picture
            hoteluser.save(update_fields=["profile_picture"])
            image_url = hoteluser.profile_picture.url if hoteluser.profile_picture else ''
            return JsonResponse({"success": True, "image_url": image_url})
        # Handle normal profile update
        name = request.POST.get('name', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        # Split name into first and last
        first_name, last_name = '', ''
        if ' ' in name:
            first_name, last_name = name.split(' ', 1)
        else:
            first_name = name
        # Uniqueness checks
        if username and username != user.username:
            if User.objects.filter(username=username).exclude(id=user.id).exists():
                messages.error(request, "Username is already taken.")
                return render(request, 'user_profile.html', {'bookings': bookings})
        if email and email != user.email:
            if User.objects.filter(email=email).exclude(id=user.id).exists():
                messages.error(request, "Email is already taken.")
                return render(request, 'user_profile.html', {'bookings': bookings})
        if phone and phone != hoteluser.phone_number:
            if HotelUser.objects.filter(phone_number=phone).exclude(id=hoteluser.id).exists():
                messages.error(request, "Phone number is already taken.")
                return render(request, 'user_profile.html', {'bookings': bookings})
        # Save changes to User model
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.save(update_fields=["first_name", "last_name", "username", "email"])
        # Save changes to HotelUser model
        hoteluser.phone_number = phone
        hoteluser.save(update_fields=["phone_number"])
        messages.success(request, "Profile updated successfully!")
        return redirect('user_profile')
    return render(request, 'user_profile.html', {'bookings': bookings})

@login_required(login_url='login_page')
def cancel_booking(request, booking_id):
    """Cancel a booking by updating its status to cancelled"""
    if not hasattr(request.user, 'hoteluser'):
        return HttpResponseForbidden("You are not authorized to view this page.")
    
    try:
        # Get the booking and ensure it belongs to the current user
        booking = HotelBooking.objects.get(id=booking_id, booking_user=request.user.hoteluser)
        
        # Only allow cancellation of upcoming bookings
        if booking.computed_status == "upcoming":
            booking.status = "cancelled"
            booking.save()
            messages.success(request, f"Booking for {booking.hotel.hotel_name} has been cancelled successfully.")
        else:
            messages.error(request, "Only upcoming bookings can be cancelled.")
            
    except HotelBooking.DoesNotExist:
        messages.error(request, "Booking not found.")
    
    return redirect('user_profile')