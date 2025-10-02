from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from Hotel.models import PersonalHotel, Habitacion
import random


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

        # Create sample rooms
        room_categories = ['Estándar', 'Superior', 'Deluxe', 'Suite']
        base_prices = {'Estándar': 50000, 'Superior': 75000, 'Deluxe': 100000, 'Suite': 150000}
        
        created_rooms = 0
        for floor in range(1, 5):  # 4 floors
            for room_num in range(1, 11):  # 10 rooms per floor
                room_number = f"{floor}{room_num:02d}"
                category = random.choice(room_categories)
                
                room, created = Habitacion.objects.get_or_create(
                    numero=room_number,
                    defaults={
                        'piso': floor,
                        'categoria': category,
                        'estado': 'Disponible',
                        'precio_diario': base_prices[category] + random.randint(-5000, 10000),
                        'descripcion': f'Habitación {category.lower()} en el piso {floor} con vista panorámica.'
                    }
                )
                if created:
                    created_rooms += 1

        if created_rooms > 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f'{created_rooms} rooms created successfully'
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