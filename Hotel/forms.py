from django import forms
from .models import Huesped, Habitacion


class HuespedForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "********"
        }),
        error_messages={
            "required": "La contraseña es obligatoria."
        }
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "********"
        }),
        error_messages={
            "required": "Debe confirmar la contraseña."
        }
    )

    class Meta:
        model = Huesped
        fields = [
            "nombre", "apellido", "email", "telefono",
            "documento_tipo", "documento_numero",
            "fecha_nacimiento", "nacionalidad"
        ]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Tu nombre"}),
            "apellido": forms.TextInput(attrs={"class": "form-control", "placeholder": "Tu apellido"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "ejemplo@correo.com"}),
            "telefono": forms.TextInput(attrs={"class": "form-control", "placeholder": "+56 9 1234 5678"}),
            "documento_tipo": forms.Select(attrs={"class": "form-control"}),
            "documento_numero": forms.TextInput(attrs={"class": "form-control", "placeholder": "Número de documento"}),
            "fecha_nacimiento": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "nacionalidad": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej: Chilena"}),
        }
        error_messages = {
            "nombre": {"required": "El nombre es obligatorio."},
            "apellido": {"required": "El apellido es obligatorio."},
            "email": {
                "required": "El correo electrónico es obligatorio.",
                "invalid": "Introduce una dirección de correo válida.",
                "unique": "Ya existe un huésped registrado con este correo."
            },
            "documento_numero": {
                "unique": "Ya existe un huésped registrado con este documento."
            },
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Las contraseñas no coinciden")

        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "ejemplo@correo.com"
        })
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "********"
        })
    )


class HabitacionForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = [
            'numero', 'piso', 'categoria', 'estado', 
            'precio_diario', 'capacidad', 'descripcion', 
            'equipamiento', 'imagen_principal'
        ]
        widgets = {
            'numero': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 101'
            }),
            'piso': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'precio_diario': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '1000',
                'min': '0'
            }),
            'capacidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 6
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción detallada de la habitación...'
            }),
            'equipamiento': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'TV, WiFi, Aire acondicionado, Minibar, etc.'
            }),
            'imagen_principal': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
        labels = {
            'numero': 'Número de Habitación',
            'piso': 'Piso',
            'categoria': 'Categoría',
            'estado': 'Estado',
            'precio_diario': 'Precio por Noche ($)',
            'capacidad': 'Capacidad (personas)',
            'descripcion': 'Descripción',
            'equipamiento': 'Equipamiento',
            'imagen_principal': 'Imagen Principal'
        }
