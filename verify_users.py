#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WaveBookApp.settings')
django.setup()

from Hotel.models import PersonalHotel
from django.contrib.auth.hashers import check_password

print("=== VERIFICACIÓN DE USUARIOS ===")

# Listar todos los usuarios
users = PersonalHotel.objects.all()
print(f"Total de usuarios: {users.count()}")

for user in users:
    print(f"\nUsuario: {user.usuario}")
    print(f"Nombre: {user.nombre} {user.apellido}")
    print(f"Rol: {user.rol}")
    print(f"Hash contraseña: {user.contrasena_hash[:50]}...")
    
    # Probar contraseñas conocidas
    passwords_to_test = {
        'admin': 'admin123',
        'mgonzalez': 'recepcion123',
        'crodriguez': 'mantenimiento123',
        'asilva': 'limpieza123'
    }
    
    if user.usuario in passwords_to_test:
        expected_password = passwords_to_test[user.usuario]
        password_valid = check_password(expected_password, user.contrasena_hash)
        print(f"Password '{expected_password}' válida: {password_valid}")
    
    print("-" * 50)

# Intentar login manual con crodriguez
print("\n=== PRUEBA DE LOGIN MANUAL ===")
try:
    staff = PersonalHotel.objects.get(usuario='crodriguez')
    password_check = check_password('mantenimiento123', staff.contrasena_hash)
    print(f"Usuario 'crodriguez' encontrado: {staff.nombre}")
    print(f"Password 'mantenimiento123' válida: {password_check}")
except PersonalHotel.DoesNotExist:
    print("Usuario 'crodriguez' NO encontrado")
except Exception as e:
    print(f"Error: {e}")