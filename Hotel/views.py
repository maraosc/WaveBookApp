from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from .forms import HuespedForm, LoginForm, HabitacionForm, ReservaForm
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
import uuid


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
def staff_required(allowed_roles=None):
    """Decorador que permite acceso a usuarios con roles específicos"""
    if allowed_roles is None:
        allowed_roles = ['Administrador']
    
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.session.get('admin_id'):
                messages.error(request, "Acceso denegado. Inicia sesión primero.")
                return redirect('admin_login')
            
            user_role = request.session.get('admin_rol')
            if user_role not in allowed_roles:
                messages.error(request, f"Acceso denegado. Tu rol ({user_role}) no tiene permisos para esta sección.")
                return redirect('admin_dashboard')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

# Decorador para compatibilidad con código existente
def admin_required(view_func):
    return staff_required(['Administrador'])(view_func)


# Admin Authentication Views
def admin_login_view(request):
    if request.method == "POST":
        usuario = request.POST.get('usuario')
        password = request.POST.get('password')
        
        if not usuario or not password:
            messages.error(request, "Por favor ingrese usuario y contraseña")
            return render(request, "admin/login.html")
        
        try:
            # Permitir login de todos los roles del personal del hotel
            staff = PersonalHotel.objects.get(usuario=usuario)
            
            if check_password(password, staff.contrasena_hash):
                request.session['admin_id'] = staff.id
                request.session['admin_nombre'] = staff.nombre
                request.session['admin_rol'] = staff.rol
                messages.success(request, f"Bienvenido {staff.nombre} ({staff.rol})")
                
                # Redirigir según el rol
                if staff.rol in ['Limpieza', 'Mantenimiento']:
                    return redirect('admin_rooms_list')
                else:
                    return redirect('admin_dashboard')
            else:
                messages.error(request, "Credenciales incorrectas")
        except PersonalHotel.DoesNotExist:
            messages.error(request, "Usuario no encontrado")
        except Exception as e:
            messages.error(request, "Error interno del sistema")
    
    return render(request, "admin/login.html")


def admin_logout_view(request):
    request.session.flush()
    messages.info(request, "Has cerrado sesión del panel administrativo")
    return redirect('admin_login')


# Admin Dashboard
@staff_required(['Administrador', 'Recepcionista'])
def admin_dashboard(request):
    # Redirigir roles operativos a habitaciones
    user_role = request.session.get('admin_rol')
    if user_role in ['Limpieza', 'Mantenimiento']:
        return redirect('admin_rooms_list')
        
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
@staff_required(['Administrador', 'Recepcionista'])
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


@staff_required(['Administrador', 'Recepcionista'])
def admin_guest_detail(request, guest_id):
    guest = get_object_or_404(Huesped, id=guest_id)
    reservas = guest.reservas.all().order_by('-fecha_creacion')
    
    return render(request, "admin/guest_detail.html", {
        'guest': guest,
        'reservas': reservas
    })


# Room Management Views
@staff_required(['Administrador', 'Mantenimiento', 'Limpieza', 'Recepcionista'])
def admin_rooms_list(request):
    user_role = request.session.get('admin_rol')
    
    # Filtrar habitaciones según el rol
    if user_role == 'Limpieza':
        # Personal de limpieza solo ve habitaciones en estado "Limpieza"
        rooms = Habitacion.objects.filter(estado='Limpieza').order_by('numero')
        role_filter = 'Limpieza'
    elif user_role == 'Mantenimiento':
        # Personal de mantenimiento solo ve habitaciones en estado "Mantenimiento"  
        rooms = Habitacion.objects.filter(estado='Mantenimiento').order_by('numero')
        role_filter = 'Mantenimiento'
    else:
        # Administrador y Recepcionista ven todas las habitaciones
        rooms = Habitacion.objects.all().order_by('numero')
        role_filter = None
        
        # Filter by status (solo para admin y recepcionista)
        status_filter = request.GET.get('status')
        if status_filter:
            rooms = rooms.filter(estado=status_filter)
    
    return render(request, "admin/rooms_list.html", {
        'rooms': rooms,
        'status_filter': request.GET.get('status') if user_role in ['Administrador', 'Recepcionista'] else None,
        'role_filter': role_filter,
        'user_role': user_role
    })


@staff_required(['Administrador', 'Mantenimiento', 'Limpieza', 'Recepcionista'])
def admin_room_detail(request, room_id):
    room = get_object_or_404(Habitacion, id=room_id)
    
    if request.method == 'POST':
        # Update room status based on user role
        new_status = request.POST.get('status')
        user_role = request.session.get('admin_rol')
        old_status = room.estado
        
        # Define allowed status changes per role
        allowed_statuses = {
            'Administrador': ['Disponible', 'Ocupada', 'Limpieza', 'Mantenimiento', 'Reservada'],
            'Mantenimiento': ['Disponible'],  # Solo puede marcar como disponible cuando ve habitaciones en mantenimiento
            'Limpieza': ['Disponible'],       # Solo puede marcar como disponible cuando ve habitaciones en limpieza
            'Recepcionista': ['Disponible', 'Ocupada', 'Limpieza', 'Reservada']  # Puede cambiar estados operativos (no mantenimiento)
        }
        
        if user_role in allowed_statuses and new_status in allowed_statuses[user_role]:
            room.estado = new_status
            room.save()
            
            # Log the change
            ReporteAuditoria.objects.create(
                tabla_afectada='Habitacion',
                id_registro=str(room.id),
                operacion='UPDATE',
                usuario_responsable=request.session.get('admin_nombre', 'Admin'),
                old_values=f"Estado anterior: {old_status}",
                new_values=f"Estado nuevo: {new_status}"
            )
            
            messages.success(request, f"Estado de habitación actualizado a {new_status}")
        else:
            messages.error(request, f"No tienes permisos para cambiar el estado a '{new_status}' con tu rol de {user_role}")
        
        return redirect('admin_room_detail', room_id=room.id)
    
    # Get current reservations for this room
    current_reservations = ReservaHabitacion.objects.filter(
        habitacion=room,
        reserva__fecha_inicio__lte=timezone.now().date(),
        reserva__fecha_fin__gte=timezone.now().date()
    ).select_related('reserva', 'reserva__huesped')
    
    return render(request, "admin/room_detail.html", {
        'room': room,
        'current_reservations': current_reservations,
        'user_role': request.session.get('admin_rol', '')
    })


@admin_required
def admin_room_edit(request, room_id):
    room = get_object_or_404(Habitacion, id=room_id)
    
    if request.method == 'POST':
        form = HabitacionForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            # Guardar valores anteriores para auditoría
            old_values = {
                'numero': room.numero,
                'piso': room.piso,
                'categoria': room.categoria,
                'estado': room.estado,
                'precio_diario': room.precio_diario,
            }
            
            updated_room = form.save()
            
            # Log the change
            ReporteAuditoria.objects.create(
                tabla_afectada='Habitacion',
                id_registro=str(room.id),
                operacion='UPDATE',
                usuario_responsable=request.session.get('admin_nombre', 'Admin'),
                old_values=json.dumps(old_values, default=str),
                new_values=json.dumps({
                    'numero': updated_room.numero,
                    'piso': updated_room.piso,
                    'categoria': updated_room.categoria,
                    'estado': updated_room.estado,
                    'precio_diario': str(updated_room.precio_diario),
                }, default=str)
            )
            
            messages.success(request, f"Habitación {updated_room.numero} actualizada exitosamente")
            return redirect('admin_room_detail', room_id=room.id)
    else:
        form = HabitacionForm(instance=room)
    
    return render(request, "admin/room_edit.html", {
        'form': form,
        'room': room
    })


@admin_required
def admin_room_create(request):
    if request.method == 'POST':
        form = HabitacionForm(request.POST, request.FILES)
        if form.is_valid():
            new_room = form.save()
            
            # Log the creation
            ReporteAuditoria.objects.create(
                tabla_afectada='Habitacion',
                id_registro=str(new_room.id),
                operacion='CREATE',
                usuario_responsable=request.session.get('admin_nombre', 'Admin'),
                new_values=json.dumps({
                    'numero': new_room.numero,
                    'piso': new_room.piso,
                    'categoria': new_room.categoria,
                    'estado': new_room.estado,
                    'precio_diario': str(new_room.precio_diario),
                }, default=str)
            )
            
            messages.success(request, f"Habitación {new_room.numero} creada exitosamente")
            return redirect('admin_room_detail', room_id=new_room.id)
    else:
        form = HabitacionForm()
    
    return render(request, "admin/room_create.html", {
        'form': form
    })


# Reservation Management Views
@staff_required(['Administrador', 'Recepcionista'])
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


@staff_required(['Administrador', 'Recepcionista'])
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


@staff_required(['Administrador', 'Recepcionista'])
def admin_reservation_create(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            try:
                # Obtener o crear huésped
                huesped_id = form.cleaned_data.get('huesped_existente')
                if huesped_id:
                    huesped = get_object_or_404(Huesped, id=huesped_id)
                else:
                    # Crear nuevo huésped
                    huesped, created = Huesped.objects.get_or_create(
                        email=form.cleaned_data['email'],
                        defaults={
                            'nombre': form.cleaned_data['nombre'],
                            'apellido': form.cleaned_data['apellido'],
                            'telefono': form.cleaned_data.get('telefono', ''),
                            'documento_tipo': form.cleaned_data['documento_tipo'],
                            'documento_numero': form.cleaned_data['documento_numero'],
                            'password': make_password('temporal123')  # Contraseña temporal
                        }
                    )
                
                # Generar código de reserva único
                codigo_reserva = f"RES-{uuid.uuid4().hex[:8].upper()}"
                
                # Calcular total
                habitaciones = form.cleaned_data['habitaciones']
                fecha_inicio = form.cleaned_data['fecha_inicio']
                fecha_fin = form.cleaned_data['fecha_fin']
                noches = (fecha_fin - fecha_inicio).days
                
                total = sum(hab.precio_diario * noches for hab in habitaciones)
                
                # Crear reserva
                reserva = Reserva.objects.create(
                    codigo_reserva=codigo_reserva,
                    huesped=huesped,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin,
                    estado='Pendiente',
                    total=total
                )
                
                # Asociar habitaciones a la reserva
                from .models import ReservaHabitacion
                for habitacion in habitaciones:
                    ReservaHabitacion.objects.create(
                        reserva=reserva,
                        habitacion=habitacion,
                        precio_por_noche=habitacion.precio_diario
                    )
                    # Marcar habitación como reservada
                    habitacion.estado = 'Reservada'
                    habitacion.save()
                
                # Registrar en auditoría
                ReporteAuditoria.objects.create(
                    tabla_afectada='Reserva',
                    id_registro=str(reserva.id),
                    operacion='CREATE',
                    usuario_responsable=request.session.get('admin_nombre', 'Admin'),
                    new_values=f"Nueva reserva {codigo_reserva} para {huesped.nombre} {huesped.apellido}"
                )
                
                messages.success(request, f"Reserva {codigo_reserva} creada exitosamente")
                return redirect('admin_reservation_detail', reservation_id=reserva.id)
                
            except Exception as e:
                messages.error(request, f"Error al crear la reserva: {str(e)}")
    else:
        form = ReservaForm()
    
    return render(request, "admin/reservation_create.html", {
        'form': form
    })


@staff_required(['Administrador', 'Recepcionista'])
def buscar_huesped_ajax(request):
    """Vista AJAX para buscar huésped por número de documento"""
    if request.method == 'GET':
        documento_numero = request.GET.get('documento', '').strip()
        
        if documento_numero:
            try:
                huesped = Huesped.objects.get(documento_numero=documento_numero)
                return JsonResponse({
                    'found': True,
                    'huesped': {
                        'id': huesped.id,
                        'nombre': huesped.nombre,
                        'apellido': huesped.apellido,
                        'email': huesped.email,
                        'telefono': huesped.telefono,
                        'documento_tipo': huesped.documento_tipo,
                        'documento_numero': huesped.documento_numero,
                        'nombre_completo': f"{huesped.nombre} {huesped.apellido}"
                    }
                })
            except Huesped.DoesNotExist:
                return JsonResponse({
                    'found': False,
                    'message': 'No se encontró ningún huésped con ese número de documento'
                })
        else:
            return JsonResponse({
                'found': False,
                'message': 'Debe proporcionar un número de documento'
            })
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)


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

def buscar_habitaciones(request):
    habitaciones_disponibles = []
    fecha_inicio = request.GET.get("fecha_inicio")
    fecha_fin = request.GET.get("fecha_fin")

    if fecha_inicio and fecha_fin:
        fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
        fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()

        # Excluir habitaciones ya reservadas en el rango
        habitaciones_disponibles = Habitacion.objects.exclude(
            id__in=ReservaHabitacion.objects.filter(
                reserva__fecha_inicio__lte=fecha_fin,
                reserva__fecha_fin__gte=fecha_inicio
            ).values_list('habitacion_id', flat=True)
        ).filter(estado='Disponible')

    if request.method == "POST":
        # Validar sesión
        if not request.session.get("huesped_id"):
            messages.warning(request, "Debe iniciar sesión para realizar una reserva.")
            return redirect("login")

        habitacion_id = request.POST.get("habitacion_id")
        fecha_inicio = datetime.strptime(request.POST.get("fecha_inicio"), "%Y-%m-%d").date()
        fecha_fin = datetime.strptime(request.POST.get("fecha_fin"), "%Y-%m-%d").date()
        dias = (fecha_fin - fecha_inicio).days or 1

        habitacion = Habitacion.objects.get(id=habitacion_id)
        huesped = Huesped.objects.get(id=request.session["huesped_id"])
        total = habitacion.precio_diario * dias

        # Crear reserva
        reserva = Reserva.objects.create(
            codigo_reserva=str(uuid.uuid4())[:8],
            huesped=huesped,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            total=total,
            estado='Pendiente'
        )

        # Asociar la habitación a la reserva
        ReservaHabitacion.objects.create(
            reserva=reserva,
            habitacion=habitacion,
            precio_por_noche=habitacion.precio_diario
        )

        # Cambiar estado de la habitación a “Reservada”
        habitacion.estado = 'Reservada'
        habitacion.save()

        messages.success(request, f"Reserva creada con éxito para la habitación {habitacion.numero}.")
        return redirect("ver_reservas")

    return render(request, "habitaciones.html", {"habitaciones": habitaciones_disponibles})


def ver_reservas(request):
    if not request.session.get("huesped_id"):
        messages.warning(request, "Debe iniciar sesión para ver sus reservas.")
        return redirect("login")

    huesped = Huesped.objects.get(id=request.session["huesped_id"])
    reservas_list = Reserva.objects.filter(huesped=huesped).order_by("-fecha_creacion")

    return render(request, "reservas.html", {"reservas": reservas_list})

def cancelar_reserva(request, reserva_id):
    if not request.session.get("huesped_id"):
        messages.warning(request, "Debe iniciar sesión para cancelar una reserva.")
        return redirect("login")

    reserva = Reserva.objects.get(id=reserva_id)
    if reserva.huesped.id != request.session["huesped_id"]:
        messages.error(request, "No puedes cancelar esta reserva.")
        return redirect("ver_reservas")

    # Cambiar estado de la reserva y liberar la habitación
    reserva.estado = "Cancelada"
    reserva.save()
    for rh in reserva.habitaciones.all():
        habitacion = rh.habitacion
        habitacion.estado = "Disponible"
        habitacion.save()

    messages.success(request, f"Reserva {reserva.codigo_reserva} cancelada correctamente.")
    return redirect("ver_reservas")