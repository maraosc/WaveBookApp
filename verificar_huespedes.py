import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WaveBookApp.settings')
django.setup()

from Hotel.models import Huesped
from django.contrib.auth.hashers import make_password

print("=== Huéspedes existentes ===")
huespedes = Huesped.objects.all()
if huespedes.exists():
    for h in huespedes[:10]:
        print(f"- {h.nombre} {h.apellido} (Doc: {h.documento_numero}, Email: {h.email})")
else:
    print("No hay huéspedes en la base de datos. Creando algunos de prueba...")
    
    # Crear huéspedes de prueba
    huespedes_prueba = [
        {
            'nombre': 'Juan',
            'apellido': 'Pérez',
            'email': 'juan.perez@email.com',
            'telefono': '+56912345678',
            'documento_tipo': 'RUT',
            'documento_numero': '12345678-9',
            'password': make_password('password123')
        },
        {
            'nombre': 'María',
            'apellido': 'González',
            'email': 'maria.gonzalez@email.com',
            'telefono': '+56987654321',
            'documento_tipo': 'RUT',
            'documento_numero': '87654321-0',
            'password': make_password('password123')
        },
        {
            'nombre': 'Carlos',
            'apellido': 'Rodríguez',
            'email': 'carlos.rodriguez@email.com',
            'telefono': '+56911223344',
            'documento_tipo': 'DNI',
            'documento_numero': '45678901',
            'password': make_password('password123')
        }
    ]
    
    for huesped_data in huespedes_prueba:
        huesped, created = Huesped.objects.get_or_create(
            email=huesped_data['email'],
            defaults=huesped_data
        )
        if created:
            print(f"✓ Creado: {huesped.nombre} {huesped.apellido} (Doc: {huesped.documento_numero})")
        else:
            print(f"- Ya existe: {huesped.nombre} {huesped.apellido} (Doc: {huesped.documento_numero})")

print("\n=== Huéspedes disponibles para búsqueda ===")
for h in Huesped.objects.all():
    print(f"Documento: {h.documento_numero} -> {h.nombre} {h.apellido} ({h.email})")