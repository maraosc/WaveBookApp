from django.db import models


class Huesped(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=150)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    documento_tipo = models.CharField(max_length=30, blank=True, null=True)
    documento_numero = models.CharField(
        max_length=50, unique=True, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class PersonalHotel(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=150)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    rol = models.CharField(max_length=50)
    usuario = models.CharField(max_length=80, unique=True)
    contrasena_hash = models.CharField(max_length=255)
    fecha_contratacion = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rol})"


class Habitacion(models.Model):
    numero = models.CharField(max_length=10, unique=True)
    piso = models.IntegerField()
    categoria = models.CharField(max_length=50)
    estado = models.CharField(max_length=30, default='Disponible')
    precio_diario = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Habitación {self.numero} - {self.categoria}"


class CatalogoHabitacion(models.Model):
    habitacion = models.ForeignKey(
        Habitacion, on_delete=models.CASCADE, related_name="catalogos")
    foto_url = models.URLField(max_length=255, blank=True, null=True)
    equipamiento = models.CharField(max_length=255, blank=True, null=True)


class Reserva(models.Model):
    codigo_reserva = models.CharField(max_length=50, unique=True)
    huesped = models.ForeignKey(
        Huesped, on_delete=models.CASCADE, related_name="reservas")
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=30, default='Pendiente')
    total = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reserva {self.codigo_reserva} ({self.huesped})"


class ReservaHabitacion(models.Model):
    reserva = models.ForeignKey(
        Reserva, on_delete=models.CASCADE, related_name="habitaciones")
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    precio_por_noche = models.DecimalField(max_digits=10, decimal_places=2)


class Pago(models.Model):
    reserva = models.ForeignKey(
        Reserva, on_delete=models.CASCADE, related_name="pagos")
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    metodo_pago = models.CharField(max_length=50)
    fecha_pago = models.DateTimeField(auto_now_add=True)


class TicketReserva(models.Model):
    reserva = models.ForeignKey(
        Reserva, on_delete=models.CASCADE, related_name="tickets")
    codigo_qr = models.CharField(max_length=255)
    fecha_emision = models.DateTimeField(auto_now_add=True)


class ReporteAuditoria(models.Model):
    tabla_afectada = models.CharField(max_length=100)
    id_registro = models.CharField(max_length=100)
    operacion = models.CharField(max_length=20)
    usuario_responsable = models.CharField(max_length=80)
    fecha = models.DateTimeField(auto_now_add=True)
    old_values = models.TextField(blank=True, null=True)
    new_values = models.TextField(blank=True, null=True)
