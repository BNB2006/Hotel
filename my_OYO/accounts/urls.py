from django.urls import path
from accounts import views

urlpatterns = [
    path('login/', views.login_page, name='login_page'),
    path('register/', views.register, name='register'),
    path('ajax-send-otp/', views.ajax_send_otp, name='ajax_send_otp'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),  # Changed to not require email in URL

    path('login-vendor/', views.login_vendor, name='login_vendor'),
    path('register-vendor/', views.register_vendor, name='register_vendor'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-hotel/', views.add_hotel, name="add_hotel"),
    path('delete_hotel/<slug>', views.delete_hotel, name="delete_hotel"),
    path('<slug>/upload-images/', views.upload_images, name="upload_images"),
    path('delete_image/<id>/', views.delete_image, name="delete_image"),
    path('edit-hotel/<slug>/', views.edit_hotel, name="edit_hotel"),
    path('bookings/', views.bookings, name="bookings"),
    path('settings/', views.vendor_settings, name="vendor_settings"),
    path('logout/', views.logout_vendor, name="logout_vendor"),

    path('verify-user/<token>/', views.verify_email_token, name="verify_email_token"),
    path('verify-vendor/<token>/', views.verify_email_token_vendor, name="verify_email_token_vendor"),
    
    # User profile and logout
    path('user-profile/', views.user_profile, name="user_profile"),
    path('logout-user/', views.logout_user, name="logout_user"),
]