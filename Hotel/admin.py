from django.contrib import admin
from .models import Huesped, PersonalHotel, Habitacion, CatalogoHabitacion, Reserva, ReservaHabitacion, Pago, TicketReserva, ReporteAuditoria

# Admin site customization
admin.site.site_header = "WaveBook - Administración del Hotel"
admin.site.site_title = "WaveBook Admin"
admin.site.index_title = "Panel de Administración"

@admin.register(Huesped)
class HuespedAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email', 'documento_tipo', 'documento_numero', 'fecha_registro')
    list_filter = ('documento_tipo', 'nacionalidad', 'fecha_registro')
    search_fields = ('nombre', 'apellido', 'email', 'documento_numero')
    readonly_fields = ('fecha_registro', 'password')
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'apellido', 'email', 'telefono')
        }),
        ('Documentación', {
            'fields': ('documento_tipo', 'documento_numero', 'nacionalidad', 'fecha_nacimiento')
        }),
        ('Sistema', {
            'fields': ('fecha_registro', 'password')
        }),
    )

@admin.register(PersonalHotel)
class PersonalHotelAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email', 'rol', 'usuario', 'fecha_contratacion')
    list_filter = ('rol', 'fecha_contratacion')
    search_fields = ('nombre', 'apellido', 'email', 'usuario')
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'apellido', 'email', 'telefono')
        }),
        ('Información Laboral', {
            'fields': ('rol', 'fecha_contratacion')
        }),
        ('Acceso al Sistema', {
            'fields': ('usuario', 'contrasena_hash')
        }),
    )

@admin.register(Habitacion)
class HabitacionAdmin(admin.ModelAdmin):
    list_display = ('numero', 'piso', 'categoria', 'estado', 'precio_diario')
    list_filter = ('piso', 'categoria', 'estado')
    search_fields = ('numero', 'categoria')
    list_editable = ('estado', 'precio_diario')
    ordering = ('numero',)

@admin.register(CatalogoHabitacion)
class CatalogoHabitacionAdmin(admin.ModelAdmin):
    list_display = ('habitacion', 'equipamiento')
    list_filter = ('habitacion__categoria', 'habitacion__piso')
    search_fields = ('habitacion__numero', 'equipamiento')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('codigo_reserva', 'huesped', 'fecha_inicio', 'fecha_fin', 'estado', 'total', 'fecha_creacion')
    list_filter = ('estado', 'fecha_inicio', 'fecha_creacion')
    search_fields = ('codigo_reserva', 'huesped__nombre', 'huesped__apellido', 'huesped__email')
    readonly_fields = ('fecha_creacion',)
    date_hierarchy = 'fecha_inicio'

@admin.register(ReservaHabitacion)
class ReservaHabitacionAdmin(admin.ModelAdmin):
    list_display = ('reserva', 'habitacion', 'precio_por_noche')
    list_filter = ('habitacion__categoria', 'habitacion__piso')
    search_fields = ('reserva__codigo_reserva', 'habitacion__numero')

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('reserva', 'monto', 'metodo_pago', 'fecha_pago')
    list_filter = ('metodo_pago', 'fecha_pago')
    search_fields = ('reserva__codigo_reserva', 'reserva__huesped__nombre')
    readonly_fields = ('fecha_pago',)
    date_hierarchy = 'fecha_pago'

@admin.register(TicketReserva)
class TicketReservaAdmin(admin.ModelAdmin):
    list_display = ('reserva', 'codigo_qr', 'fecha_emision')
    search_fields = ('reserva__codigo_reserva', 'codigo_qr')
    readonly_fields = ('fecha_emision',)

@admin.register(ReporteAuditoria)
class ReporteAuditoriaAdmin(admin.ModelAdmin):
    list_display = ('tabla_afectada', 'id_registro', 'operacion', 'usuario_responsable', 'fecha')
    list_filter = ('tabla_afectada', 'operacion', 'fecha')
    search_fields = ('tabla_afectada', 'id_registro', 'usuario_responsable')
    readonly_fields = ('fecha',)
    date_hierarchy = 'fecha'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
