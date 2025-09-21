from django import forms
from .models import Huesped


class HuespedForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "********"})
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "********"})
    )

    class Meta:
        model = Huesped
        fields = [
            "nombre", "apellido", "email", "telefono",
            "documento_tipo", "documento_numero",
            "fecha_nacimiento", "nacionalidad"
        ]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "apellido": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
            "documento_tipo": forms.Select(attrs={"class": "form-control"}),
            "documento_numero": forms.TextInput(attrs={"class": "form-control"}),
            "fecha_nacimiento": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "nacionalidad": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            self.add_error("password2", "Las contraseñas no coinciden")
        return cleaned_data
