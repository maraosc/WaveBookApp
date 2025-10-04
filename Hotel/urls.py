from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    
    # Test URL
    path("test-admin/", views.test_admin_view, name="test_admin"),
    
    # Hotel Admin URLs (using 'hotel-admin' to avoid conflict with Django admin)
    path("hotel-admin/login/", views.admin_login_view, name="admin_login"),
    path("hotel-admin/logout/", views.admin_logout_view, name="admin_logout"),
    path("hotel-admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    
    # Guest Management
    path("hotel-admin/guests/", views.admin_guests_list, name="admin_guests_list"),
    path("hotel-admin/guests/<int:guest_id>/", views.admin_guest_detail, name="admin_guest_detail"),
    
    # Room Management
    path("hotel-admin/rooms/", views.admin_rooms_list, name="admin_rooms_list"),
    path("hotel-admin/rooms/create/", views.admin_room_create, name="admin_room_create"),
    path("hotel-admin/rooms/<int:room_id>/", views.admin_room_detail, name="admin_room_detail"),
    path("hotel-admin/rooms/<int:room_id>/edit/", views.admin_room_edit, name="admin_room_edit"),
    
    # Reservation Management
    path("hotel-admin/reservations/", views.admin_reservations_list, name="admin_reservations_list"),
    path("hotel-admin/reservations/<int:reservation_id>/", views.admin_reservation_detail, name="admin_reservation_detail"),
    
    # Staff Management
    path("hotel-admin/staff/", views.admin_staff_list, name="admin_staff_list"),
    path("hotel-admin/staff/<int:staff_id>/", views.admin_staff_detail, name="admin_staff_detail"),
    
    # Reports
    path("hotel-admin/reports/", views.admin_reports, name="admin_reports"),
    path("hotel-admin/audit/", views.admin_audit_log, name="admin_audit_log"),
]
