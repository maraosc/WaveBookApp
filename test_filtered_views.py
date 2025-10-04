#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WaveBookApp.settings')
django.setup()

from Hotel.models import Habitacion

def setup_demo_rooms():
    """Configurar algunas habitaciones en diferentes estados para demostrar los filtros"""
    
    # Cambiar algunas habitaciones a estado Limpieza
    rooms_for_cleaning = Habitacion.objects.filter(numero__in=['101', '102', '201'])
    for room in rooms_for_cleaning:
        room.estado = 'Limpieza'
        room.save()
    
    # Cambiar algunas habitaciones a estado Mantenimiento  
    rooms_for_maintenance = Habitacion.objects.filter(numero__in=['301', '302', '401'])
    for room in rooms_for_maintenance:
        room.estado = 'Mantenimiento'
        room.save()
    
    # Cambiar algunas habitaciones a estado Ocupada
    rooms_occupied = Habitacion.objects.filter(numero__in=['103', '203', '303'])
    for room in rooms_occupied:
        room.estado = 'Ocupada'
        room.save()

def show_filtered_view_info():
    print("=== SISTEMA DE FILTROS POR ROL IMPLEMENTADO ===\n")
    
    # Configurar habitaciones de demostración
    setup_demo_rooms()
    
    print("🎯 **NUEVA FUNCIONALIDAD: VISTAS FILTRADAS**")
    print("   • Personal de Limpieza solo ve habitaciones en estado 'Limpieza'")
    print("   • Personal de Mantenimiento solo ve habitaciones en estado 'Mantenimiento'")
    print("   • Solo pueden marcar como 'Disponible' cuando terminan su trabajo")
    print()
    
    # Mostrar estadísticas actuales
    limpieza_count = Habitacion.objects.filter(estado='Limpieza').count()
    mantenimiento_count = Habitacion.objects.filter(estado='Mantenimiento').count()
    ocupada_count = Habitacion.objects.filter(estado='Ocupada').count()
    disponible_count = Habitacion.objects.filter(estado='Disponible').count()
    
    print("📊 **ESTADO ACTUAL DE HABITACIONES:**")
    print(f"   🧹 En Limpieza: {limpieza_count} habitaciones")
    print(f"   🔧 En Mantenimiento: {mantenimiento_count} habitaciones") 
    print(f"   👥 Ocupadas: {ocupada_count} habitaciones")
    print(f"   ✅ Disponibles: {disponible_count} habitaciones")
    print()
    
    print("🔑 **COMPORTAMIENTO POR ROL:**")
    print()
    
    print("🧹 **PERSONAL DE LIMPIEZA (asilva/limpieza123):**")
    if limpieza_count > 0:
        limpieza_rooms = list(Habitacion.objects.filter(estado='Limpieza').values_list('numero', flat=True))
        print(f"   • Ve SOLO estas habitaciones: {', '.join(limpieza_rooms)}")
    else:
        print("   • No ve ninguna habitación (no hay habitaciones en limpieza)")
    print("   • Puede marcar como 'Disponible' cuando termine la limpieza")
    print("   • Botón grande: 'Limpieza Terminada'")
    print()
    
    print("🔧 **PERSONAL DE MANTENIMIENTO (crodriguez/mantenimiento123):**")
    if mantenimiento_count > 0:
        maintenance_rooms = list(Habitacion.objects.filter(estado='Mantenimiento').values_list('numero', flat=True))
        print(f"   • Ve SOLO estas habitaciones: {', '.join(maintenance_rooms)}")
    else:
        print("   • No ve ninguna habitación (no hay habitaciones en mantenimiento)")
    print("   • Puede marcar como 'Disponible' cuando termine las reparaciones")
    print("   • Botón grande: 'Reparación Terminada'")
    print()
    
    print("👑 **ADMINISTRADOR (admin/admin123):**")
    print("   • Ve TODAS las habitaciones")
    print("   • Puede usar filtros por estado")
    print("   • Puede cambiar a cualquier estado")
    print("   • Puede crear nuevas habitaciones")
    print()
    
    print("📞 **RECEPCIONISTA (mgonzalez/recepcion123):**")
    print("   • Ve TODAS las habitaciones")
    print("   • Puede usar filtros por estado")
    print("   • Solo visualización (no puede cambiar estados)")
    print()
    
    print("🎯 **FLUJO DE TRABAJO OPTIMIZADO:**")
    print("   1. Admin/Recepcionista marca habitación como 'Limpieza' o 'Mantenimiento'")
    print("   2. Personal especializado solo ve habitaciones de su área")
    print("   3. Trabajador marca como 'Disponible' al terminar")
    print("   4. Habitación vuelve a estar disponible para huéspedes")
    print()
    
    print("=== INSTRUCCIONES DE PRUEBA ===")
    print("1. Inicia sesión como personal de limpieza (asilva/limpieza123)")
    print("2. Observa que solo ves habitaciones en estado 'Limpieza'")
    print("3. Marca una como 'Limpieza Terminada'")
    print("4. Inicia sesión como mantenimiento (crodriguez/mantenimiento123)")
    print("5. Observa que solo ves habitaciones en estado 'Mantenimiento'")
    print("6. Marca una como 'Reparación Terminada'")
    print("7. Inicia sesión como admin para ver todas las habitaciones")

if __name__ == "__main__":
    show_filtered_view_info()