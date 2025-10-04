#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WaveBookApp.settings')
django.setup()

from Hotel.models import PersonalHotel

def show_role_behavior():
    print("=== COMPORTAMIENTO DEL SISTEMA POR ROLES ===\n")
    
    roles_info = {
        'Administrador': {
            'usuario': 'admin',
            'password': 'admin123',
            'login_redirect': '/admin/dashboard/',
            'sidebar_menu': [
                'Dashboard',
                'Huéspedes', 
                'Habitaciones',
                'Reservas',
                'Personal',
                'Reportes',
                'Auditoría'
            ],
            'permissions': [
                'Acceso completo al sistema',
                'Puede ver y editar habitaciones',
                'Puede cambiar cualquier estado de habitación',
                'Acceso a reportes y auditoría',
                'Gestión de personal y reservas'
            ]
        },
        'Recepcionista': {
            'usuario': 'mgonzalez',
            'password': 'recepcion123',
            'login_redirect': '/admin/dashboard/',
            'sidebar_menu': [
                'Dashboard',
                'Huéspedes',
                'Habitaciones',
                'Reservas'
            ],
            'permissions': [
                'Acceso al dashboard con estadísticas',
                'Puede ver huéspedes y reservas',
                'Puede ver habitaciones (solo lectura)',
                'No puede cambiar estados de habitaciones',
                'No acceso a Personal, Reportes ni Auditoría'
            ]
        },
        'Mantenimiento': {
            'usuario': 'crodriguez',
            'password': 'mantenimiento123',
            'login_redirect': '/admin/rooms/',
            'sidebar_menu': [
                'Habitaciones (únicamente)'
            ],
            'permissions': [
                'Redirigido automáticamente a Habitaciones',
                'Solo ve el menú de Habitaciones',
                'Puede cambiar estado: Disponible ↔ Mantenimiento',
                'No puede editar configuración de habitaciones',
                'Acceso denegado a otras secciones'
            ]
        },
        'Limpieza': {
            'usuario': 'asilva',
            'password': 'limpieza123',
            'login_redirect': '/admin/rooms/',
            'sidebar_menu': [
                'Habitaciones (únicamente)'
            ],
            'permissions': [
                'Redirigido automáticamente a Habitaciones',
                'Solo ve el menú de Habitaciones',
                'Puede cambiar estado: Disponible ↔ Ocupada',
                'No puede editar configuración de habitaciones',
                'Acceso denegado a otras secciones'
            ]
        }
    }
    
    for rol, info in roles_info.items():
        print(f"🔹 {rol.upper()}")
        print(f"   👤 Usuario: {info['usuario']}")
        print(f"   🔑 Contraseña: {info['password']}")
        print(f"   🏠 Redirección tras login: {info['login_redirect']}")
        print(f"   📋 Menú lateral:")
        for menu_item in info['sidebar_menu']:
            print(f"      • {menu_item}")
        print(f"   ✅ Permisos:")
        for permission in info['permissions']:
            print(f"      • {permission}")
        print("-" * 60)
    
    print("\n=== INSTRUCCIONES DE PRUEBA ===")
    print("1. Abre http://127.0.0.1:8000/admin/login")
    print("2. Prueba con diferentes usuarios:")
    print("   - Observa cómo cambia la página de destino tras login")
    print("   - Verifica que el menú lateral sea diferente por rol")
    print("   - Intenta acceder manualmente a URLs restringidas")
    print("3. Roles operativos (Limpieza/Mantenimiento):")
    print("   - Son redirigidos automáticamente a habitaciones")
    print("   - Solo ven 'Habitaciones' en el menú lateral")
    print("   - No pueden acceder a Dashboard, Huéspedes, etc.")
    print("4. Recepcionista:")
    print("   - Ve dashboard y puede gestionar huéspedes/reservas")
    print("   - No ve opciones administrativas (Personal, Reportes)")
    print("5. Administrador:")
    print("   - Acceso completo a todas las funcionalidades")

if __name__ == "__main__":
    show_role_behavior()