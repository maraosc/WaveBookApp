#!/usr/bin/env python
"""
Script para probar el acceso por roles en el sistema admin de WaveBook
"""
import os
import django
import sys

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WaveBookApp.settings')
django.setup()

from Hotel.models import PersonalHotel, Habitacion

def test_login_credentials():
    """Mostrar todos los usuarios disponibles para login"""
    print("=== USUARIOS DISPONIBLES PARA LOGIN ===")
    staff = PersonalHotel.objects.all()
    
    for person in staff:
        print(f"Usuario: {person.usuario}")
        print(f"Contraseña: {person.contrasena_hash[:20]}...")
        print(f"Nombre: {person.nombre} {person.apellido}")
        print(f"Rol: {person.rol}")
        print(f"Correo: {person.email}")
        print("-" * 40)

def test_room_statistics():
    """Mostrar estadísticas de habitaciones"""
    print("\n=== ESTADÍSTICAS DE HABITACIONES ===")
    rooms = Habitacion.objects.all()
    
    # Contar por estado
    estados = {}
    for room in rooms:
        estado = room.estado
        if estado in estados:
            estados[estado] += 1
        else:
            estados[estado] = 1
    
    print("Estados de habitaciones:")
    for estado, count in estados.items():
        print(f"  {estado}: {count} habitaciones")
    
    print(f"\nTotal de habitaciones: {rooms.count()}")
    
    # Contar por categoría
    categorias = {}
    for room in rooms:
        categoria = room.categoria
        if categoria in categorias:
            categorias[categoria] += 1
        else:
            categorias[categoria] = 1
    
    print("\nCategorías de habitaciones:")
    for categoria, count in categorias.items():
        print(f"  {categoria}: {count} habitaciones")

def test_role_permissions():
    """Mostrar los permisos por rol"""
    print("\n=== PERMISOS POR ROL ===")
    
    permissions = {
        'Administrador': [
            'Acceso completo al sistema',
            'Puede editar habitaciones',
            'Puede cambiar estado a cualquier valor: Disponible, Ocupada, Mantenimiento, Reservada',
            'Puede ver todos los reportes y auditoría',
            'Puede gestionar huéspedes y reservas'
        ],
        'Mantenimiento': [
            'Acceso al panel de habitaciones',
            'Solo puede cambiar estado entre: Disponible ↔ Mantenimiento',
            'Puede ver detalles de habitaciones',
            'No puede editar habitaciones',
            'No puede crear nuevas habitaciones'
        ],
        'Limpieza': [
            'Acceso al panel de habitaciones',
            'Solo puede cambiar estado entre: Disponible ↔ Ocupada',
            'Puede ver detalles de habitaciones',
            'No puede editar habitaciones',
            'No puede crear nuevas habitaciones'
        ],
        'Recepcionista': [
            'Acceso al panel de habitaciones',
            'Solo puede VER estados de habitaciones',
            'No puede cambiar ningún estado',
            'No puede editar habitaciones',
            'No puede crear nuevas habitaciones',
            'Acceso de solo lectura para consultas de huéspedes'
        ]
    }
    
    for rol, permisos in permissions.items():
        print(f"\n{rol.upper()}:")
        for permiso in permisos:
            print(f"  ✓ {permiso}")

if __name__ == "__main__":
    test_login_credentials()
    test_room_statistics()
    test_role_permissions()
    
    print("\n=== INSTRUCCIONES DE PRUEBA ===")
    print("1. Abre http://127.0.0.1:8000/admin/login en tu navegador")
    print("2. Prueba el login con diferentes usuarios:")
    print("   - admin / admin123 (Administrador) - Acceso completo")
    print("   - crodriguez / mantenimiento123 (Mantenimiento) - Solo habitaciones con permisos limitados")
    print("   - asilva / limpieza123 (Limpieza) - Solo habitaciones con permisos de limpieza")
    print("   - mgonzalez / recepcion123 (Recepcionista) - Solo habitaciones con permisos de visualización")
    print("3. Verifica que cada rol solo vea los botones de cambio de estado permitidos")
    print("4. Intenta cambiar estados no permitidos para verificar la validación")
    print("5. Observa que el nombre y rol del usuario aparecen en la barra superior")