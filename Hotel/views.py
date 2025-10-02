from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from .forms import HuespedForm, LoginForm
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count, Sum
from django.utils import timezone
from datetime import datetime, timedelta
from .models import (
    Huesped, PersonalHotel, Habitacion, CatalogoHabitacion, 
    Reserva, ReservaHabitacion, Pago, TicketReserva, ReporteAuditoria
)
from django.contrib.auth.decorators import login_required
import json


def home(request):
    return render(request, "home.html")


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            try:
                huesped = Huesped.objects.get(email=email)
                if check_password(password, huesped.password):
                    request.session["huesped_id"] = huesped.id
                    request.session["huesped_nombre"] = huesped.nombre
                    messages.success(request, f"Bienvenido {huesped.nombre} 👋")
                    return redirect("home")
                else:
                    form.add_error("password", "Contraseña incorrecta ❌")
            except Huesped.DoesNotExist:
                form.add_error("email", "Este correo no está registrado")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


def logout_view(request):
    request.session.flush()  # elimina toda la sesión
    messages.info(request, "Has cerrado sesión 👋")
    return redirect("home")


def register_view(request):
    if request.method == "POST":
        form = HuespedForm(request.POST)
        if form.is_valid():
            huesped = form.save(commit=False)
            huesped.password = form.cleaned_data["password1"]
            huesped.save()

            # Iniciar sesión automáticamente
            request.session["huesped_id"] = huesped.id
            request.session["huesped_nombre"] = huesped.nombre

            # Mensaje de bienvenida
            messages.success(
                request, f"¡Bienvenido {huesped.nombre} 👋 Tu cuenta fue creada con éxito!")

            return redirect("home")  # va al inicio con sesión iniciada
    else:
        form = HuespedForm()

    return render(request, "register.html", {"form": form})


# Test view to check if URLs work
def test_admin_view(request):
    return HttpResponse("<h1>Test Admin View Works!</h1><p>This confirms URLs are working.</p><a href='/hotel-admin/login/'>Go to Hotel Admin Login</a>")


# Admin session middleware
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('admin_id'):
            messages.error(request, "Acceso denegado. Inicia sesión como administrador.")
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return wrapper


# Admin Authentication Views
def admin_login_view(request):
    print(f"DEBUG: admin_login_view called - Method: {request.method}")
    print(f"DEBUG: Request path: {request.path}")
    print(f"DEBUG: POST data: {dict(request.POST)}")
    
    if request.method == "POST":
        usuario = request.POST.get('usuario')
        password = request.POST.get('password')
        
        print(f"DEBUG: Login attempt - Usuario: '{usuario}', Password length: {len(password) if password else 0}")
        
        if not usuario or not password:
            print("DEBUG: Missing usuario or password")
            messages.error(request, "Por favor ingrese usuario y contraseña")
            return render(request, "admin/login.html")
        
        try:
            admin = PersonalHotel.objects.get(usuario=usuario, rol='Administrador')
            print(f"DEBUG: Found admin user: {admin.nombre}")
            
            if check_password(password, admin.contrasena_hash):
                print("DEBUG: Password check successful")
                request.session['admin_id'] = admin.id
                request.session['admin_nombre'] = admin.nombre
                request.session['admin_rol'] = admin.rol
                messages.success(request, f"Bienvenido {admin.nombre}")
                print("DEBUG: Redirecting to admin_dashboard")
                return redirect('admin_dashboard')
            else:
                print("DEBUG: Password check failed")
                messages.error(request, "Credenciales incorrectas")
        except PersonalHotel.DoesNotExist:
            print(f"DEBUG: Admin user not found: {usuario}")
            messages.error(request, "Usuario no encontrado")
        except Exception as e:
            print(f"DEBUG: Unexpected error: {e}")
            messages.error(request, "Error interno del sistema")
    else:
        print("DEBUG: GET request - showing login form")
    
    return render(request, "admin/login.html")


def admin_logout_view(request):
    request.session.flush()
    messages.info(request, "Has cerrado sesión del panel administrativo")
    return redirect('admin_login')


# Admin Dashboard
@admin_required
def admin_dashboard(request):
    # Estadísticas generales
    total_huespedes = Huesped.objects.count()
    total_habitaciones = Habitacion.objects.count()
    habitaciones_ocupadas = Habitacion.objects.filter(estado='Ocupada').count()
    reservas_pendientes = Reserva.objects.filter(estado='Pendiente').count()
    
    # Ingresos del mes actual
    current_month = timezone.now().month
    ingresos_mes = Pago.objects.filter(
        fecha_pago__month=current_month
    ).aggregate(total=Sum('monto'))['total'] or 0
    
    # Reservas recientes
    reservas_recientes = Reserva.objects.select_related('huesped').order_by('-fecha_creacion')[:5]
    
    context = {
        'total_huespedes': total_huespedes,
        'total_habitaciones': total_habitaciones,
        'habitaciones_ocupadas': habitaciones_ocupadas,
        'habitaciones_disponibles': total_habitaciones - habitaciones_ocupadas,
        'reservas_pendientes': reservas_pendientes,
        'ingresos_mes': ingresos_mes,
        'reservas_recientes': reservas_recientes,
    }
    
    return render(request, "admin/dashboard.html", context)


# Guest Management Views
@admin_required
def admin_guests_list(request):
    search_query = request.GET.get('search', '')
    guests = Huesped.objects.all()
    
    if search_query:
        guests = guests.filter(
            Q(nombre__icontains=search_query) |
            Q(apellido__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(documento_numero__icontains=search_query)
        )
    
    paginator = Paginator(guests, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "admin/guests_list.html", {
        'page_obj': page_obj,
        'search_query': search_query
    })


@admin_required
def admin_guest_detail(request, guest_id):
    guest = get_object_or_404(Huesped, id=guest_id)
    reservas = guest.reservas.all().order_by('-fecha_creacion')
    
    return render(request, "admin/guest_detail.html", {
        'guest': guest,
        'reservas': reservas
    })


# Room Management Views
@admin_required
def admin_rooms_list(request):
    rooms = Habitacion.objects.all().order_by('numero')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        rooms = rooms.filter(estado=status_filter)
    
    return render(request, "admin/rooms_list.html", {
        'rooms': rooms,
        'status_filter': status_filter
    })


@admin_required
def admin_room_detail(request, room_id):
    room = get_object_or_404(Habitacion, id=room_id)
    
    if request.method == 'POST':
        # Update room status
        new_status = request.POST.get('status')
        if new_status in ['Disponible', 'Ocupada', 'Mantenimiento', 'Fuera de servicio']:
            room.estado = new_status
            room.save()
            
            # Log the change
            ReporteAuditoria.objects.create(
                tabla_afectada='Habitacion',
                id_registro=str(room.id),
                operacion='UPDATE',
                usuario_responsable=request.session.get('admin_nombre', 'Admin'),
                old_values=f"Estado anterior: {room.estado}",
                new_values=f"Estado nuevo: {new_status}"
            )
            
            messages.success(request, f"Estado de habitación actualizado a {new_status}")
            return redirect('admin_room_detail', room_id=room.id)
    
    # Get current reservations for this room
    current_reservations = ReservaHabitacion.objects.filter(
        habitacion=room,
        reserva__fecha_inicio__lte=timezone.now().date(),
        reserva__fecha_fin__gte=timezone.now().date()
    ).select_related('reserva', 'reserva__huesped')
    
    return render(request, "admin/room_detail.html", {
        'room': room,
        'current_reservations': current_reservations
    })


# Reservation Management Views
@admin_required
def admin_reservations_list(request):
    reservations = Reserva.objects.select_related('huesped').order_by('-fecha_creacion')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        reservations = reservations.filter(estado=status_filter)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        reservations = reservations.filter(
            Q(codigo_reserva__icontains=search_query) |
            Q(huesped__nombre__icontains=search_query) |
            Q(huesped__apellido__icontains=search_query)
        )
    
    paginator = Paginator(reservations, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "admin/reservations_list.html", {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'search_query': search_query
    })


@admin_required
def admin_reservation_detail(request, reservation_id):
    reservation = get_object_or_404(Reserva, id=reservation_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'confirm':
            reservation.estado = 'Confirmada'
            reservation.save()
            messages.success(request, "Reserva confirmada")
        elif action == 'cancel':
            reservation.estado = 'Cancelada'
            reservation.save()
            # Free up the rooms
            ReservaHabitacion.objects.filter(reserva=reservation).delete()
            messages.success(request, "Reserva cancelada")
        elif action == 'checkin':
            reservation.estado = 'En curso'
            reservation.save()
            # Mark rooms as occupied
            for reserva_hab in reservation.habitaciones.all():
                reserva_hab.habitacion.estado = 'Ocupada'
                reserva_hab.habitacion.save()
            messages.success(request, "Check-in realizado")
        elif action == 'checkout':
            reservation.estado = 'Completada'
            reservation.save()
            # Mark rooms as available
            for reserva_hab in reservation.habitaciones.all():
                reserva_hab.habitacion.estado = 'Disponible'
                reserva_hab.habitacion.save()
            messages.success(request, "Check-out realizado")
        
        return redirect('admin_reservation_detail', reservation_id=reservation.id)
    
    rooms = reservation.habitaciones.all()
    payments = reservation.pagos.all()
    
    return render(request, "admin/reservation_detail.html", {
        'reservation': reservation,
        'rooms': rooms,
        'payments': payments
    })


# Staff Management Views
@admin_required
def admin_staff_list(request):
    staff = PersonalHotel.objects.all().order_by('apellido')
    
    return render(request, "admin/staff_list.html", {
        'staff': staff
    })


@admin_required
def admin_staff_detail(request, staff_id):
    staff_member = get_object_or_404(PersonalHotel, id=staff_id)
    
    return render(request, "admin/staff_detail.html", {
        'staff_member': staff_member
    })


# Reports Views
@admin_required
def admin_reports(request):
    # Date range filters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if not start_date:
        start_date = (timezone.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    if not end_date:
        end_date = timezone.now().strftime('%Y-%m-%d')
    
    # Revenue report
    payments = Pago.objects.filter(
        fecha_pago__date__range=[start_date, end_date]
    )
    total_revenue = payments.aggregate(total=Sum('monto'))['total'] or 0
    
    # Occupancy rate
    total_days = (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days + 1
    total_room_days = Habitacion.objects.count() * total_days
    occupied_room_days = ReservaHabitacion.objects.filter(
        reserva__fecha_inicio__lte=end_date,
        reserva__fecha_fin__gte=start_date
    ).count()
    occupancy_rate = (occupied_room_days / total_room_days * 100) if total_room_days > 0 else 0
    
    # Popular rooms
    popular_rooms = Habitacion.objects.annotate(
        reservation_count=Count('reservahabitacion')
    ).order_by('-reservation_count')[:5]
    
    context = {
        'start_date': start_date,
        'end_date': end_date,
        'total_revenue': total_revenue,
        'occupancy_rate': round(occupancy_rate, 2),
        'popular_rooms': popular_rooms,
        'payments': payments[:10]  # Recent payments
    }
    
    return render(request, "admin/reports.html", context)


# Audit Reports
@admin_required
def admin_audit_log(request):
    logs = ReporteAuditoria.objects.all().order_by('-fecha')
    
    paginator = Paginator(logs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "admin/audit_log.html", {
        'page_obj': page_obj
    })
