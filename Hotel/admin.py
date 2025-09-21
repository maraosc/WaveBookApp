from django.contrib import admin
from .models import Huesped, PersonalHotel, Habitacion, CatalogoHabitacion, Reserva, ReservaHabitacion, Pago, TicketReserva, ReporteAuditoria

admin.site.register([Huesped, PersonalHotel, Habitacion, CatalogoHabitacion,
                     Reserva, ReservaHabitacion, Pago, TicketReserva, ReporteAuditoria])
