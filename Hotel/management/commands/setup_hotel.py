from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from Hotel.models import PersonalHotel, Habitacion


class Command(BaseCommand):
    help = 'Create admin user and sample data for WaveBook Hotel'

    def handle(self, *args, **options):
        # Create admin user
        admin_user, created = PersonalHotel.objects.get_or_create(
            usuario='admin',
            defaults={
                'nombre': 'Administrador',
                'apellido': 'Sistema',
                'email': 'admin@wavebook.com',
                'telefono': '+56912345678',
                'rol': 'Administrador',
                'contrasena_hash': make_password('admin123'),
                'fecha_contratacion': '2024-01-01'
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Admin user created: {admin_user.usuario}'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f'Admin user already exists: {admin_user.usuario}'
                )
            )

        # Create sample staff
        staff_data = [
            {
                'nombre': 'María',
                'apellido': 'González',
                'email': 'maria.gonzalez@wavebook.com',
                'telefono': '+56987654321',
                'rol': 'Recepcionista',
                'usuario': 'mgonzalez',
                'contrasena_hash': make_password('recepcion123'),
                'fecha_contratacion': '2024-02-01'
            },
            {
                'nombre': 'Carlos',
                'apellido': 'Rodriguez',
                'email': 'carlos.rodriguez@wavebook.com',
                'telefono': '+56912345679',
                'rol': 'Mantenimiento',
                'usuario': 'crodriguez',
                'contrasena_hash': make_password('mantenimiento123'),
                'fecha_contratacion': '2024-01-15'
            },
            {
                'nombre': 'Ana',
                'apellido': 'Silva',
                'email': 'ana.silva@wavebook.com',
                'telefono': '+56987654322',
                'rol': 'Limpieza',
                'usuario': 'asilva',
                'contrasena_hash': make_password('limpieza123'),
                'fecha_contratacion': '2024-03-01'
            }
        ]

        for staff_info in staff_data:
            staff_member, created = PersonalHotel.objects.get_or_create(
                usuario=staff_info['usuario'],
                defaults=staff_info
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Staff member created: {staff_member.nombre} {staff_member.apellido} ({staff_member.rol})'
                    )
                )

        # Create all 38 rooms according to hotel structure
        # Eliminar habitaciones existentes para recrearlas con la estructura correcta
        Habitacion.objects.all().delete()
        
        created_rooms = 0
        
        # Pisos 1-5: 6 habitaciones cada uno - Categoría Turista (30 habitaciones)
        for piso in range(1, 6):  # Pisos 1, 2, 3, 4, 5
            for habitacion in range(1, 7):  # Habitaciones 1, 2, 3, 4, 5, 6
                numero = f"{piso}{habitacion:02d}"  # Formato: 101, 102, 103, etc.
                
                room, created = Habitacion.objects.get_or_create(
                    numero=numero,
                    defaults={
                        'piso': piso,
                        'categoria': 'Turista',
                        'estado': 'Disponible',
                        'precio_diario': 85000,
                        'descripcion': f'Habitación turista en piso {piso} con comodidades estándar, baño privado, TV y WiFi.'
                    }
                )
                if created:
                    created_rooms += 1
        
        # Pisos 6-7: 4 habitaciones cada uno - Categoría Premium (8 habitaciones)
        for piso in range(6, 8):  # Pisos 6, 7
            for habitacion in range(1, 5):  # Habitaciones 1, 2, 3, 4
                numero = f"{piso}{habitacion:02d}"  # Formato: 601, 602, 603, etc.
                
                room, created = Habitacion.objects.get_or_create(
                    numero=numero,
                    defaults={
                        'piso': piso,
                        'categoria': 'Premium',
                        'estado': 'Disponible',
                        'precio_diario': 180000,
                        'descripcion': f'Suite Premium en piso {piso} con vista panorámica, jacuzzi, minibar, servicio a la habitación 24/7 y servicios exclusivos.'
                    }
                )
                if created:
                    created_rooms += 1

        if created_rooms > 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f'{created_rooms} habitaciones creadas exitosamente\n'
                    f'Estructura del hotel:\n'
                    f'  - Pisos 1-5: 30 habitaciones Turista ($85.000/noche)\n'
                    f'  - Pisos 6-7: 8 habitaciones Premium ($180.000/noche)\n'
                    f'  - Total: 38 habitaciones'
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                'Setup completed!\n'
                'Admin credentials:\n'
                '  Username: admin\n'
                '  Password: admin123\n\n'
                'Access the admin panel at: /admin/login/\n'
                'Access the hotel admin at: /admin/login/ (using admin credentials)'
            )
        )