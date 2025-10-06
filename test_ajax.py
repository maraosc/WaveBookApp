import os
import django
import requests

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WaveBookApp.settings')
django.setup()

from Hotel.models import PersonalHotel

# Probar la vista AJAX directamente
print("=== Prueba de vista AJAX ===")

# Verificar si tenemos personal administrativo
admin_users = PersonalHotel.objects.filter(rol='Administrador')
if admin_users.exists():
    admin = admin_users.first()
    print(f"Usuario admin encontrado: {admin.nombre} {admin.apellido}")
else:
    print("No hay usuarios administradores")

# Probar la URL directamente
url = "http://127.0.0.1:8000/hotel-admin/ajax/buscar-huesped/?documento=123456789-1"
print(f"Probando URL: {url}")

try:
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")