#!/usr/bin/env python
import os
import sys
import django
from django.test import Client

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WaveBookApp.settings')
django.setup()

def test_login():
    print("=== PRUEBA DE LOGIN CON DJANGO TEST CLIENT ===")
    
    client = Client()
    
    # Lista de usuarios para probar
    users_to_test = [
        ('admin', 'admin123', 'Administrador'),
        ('crodriguez', 'mantenimiento123', 'Mantenimiento'), 
        ('asilva', 'limpieza123', 'Limpieza'),
        ('mgonzalez', 'recepcion123', 'Recepcionista')
    ]
    
    for usuario, password, rol in users_to_test:
        print(f"\n--- Probando login con {usuario} ({rol}) ---")
        
        # Hacer GET para obtener el formulario
        response = client.get('/admin/login/')
        print(f"GET /admin/login/ - Status: {response.status_code}")
        
        # Hacer POST para login
        response = client.post('/admin/login/', {
            'usuario': usuario,
            'password': password
        })
        
        print(f"POST /admin/login/ - Status: {response.status_code}")
        
        if response.status_code == 302:  # Redirect significa login exitoso
            print(f"✅ LOGIN EXITOSO - Redirigido a: {response.url}")
            
            # Verificar sesión
            session = client.session
            print(f"   Session admin_id: {session.get('admin_id')}")
            print(f"   Session admin_nombre: {session.get('admin_nombre')}")
            print(f"   Session admin_rol: {session.get('admin_rol')}")
            
            # Hacer logout para la siguiente prueba
            client.logout()
            
        else:
            print(f"❌ LOGIN FALLIDO - Status: {response.status_code}")
            print(f"   Content: {response.content.decode()[:200]}...")

if __name__ == "__main__":
    test_login()