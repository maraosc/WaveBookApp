from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .forms import HuespedForm, LoginForm
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import Huesped


def home(request):
    return render(request, "home.html")


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            try:
                huesped = Huesped.objects.get(email=email)
                if check_password(password, huesped.password):
                    request.session["huesped_id"] = huesped.id
                    request.session["huesped_nombre"] = huesped.nombre
                    messages.success(request, f"Bienvenido {huesped.nombre} 👋")
                    return redirect("home")
                else:
                    form.add_error("password", "Contraseña incorrecta ❌")
            except Huesped.DoesNotExist:
                form.add_error("email", "Este correo no está registrado")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


def logout_view(request):
    request.session.flush()  # elimina toda la sesión
    messages.info(request, "Has cerrado sesión 👋")
    return redirect("home")


def register_view(request):
    if request.method == "POST":
        form = HuespedForm(request.POST)
        if form.is_valid():
            huesped = form.save(commit=False)
            huesped.password = form.cleaned_data["password1"]
            huesped.save()

            # Iniciar sesión automáticamente
            request.session["huesped_id"] = huesped.id
            request.session["huesped_nombre"] = huesped.nombre

            # Mensaje de bienvenida
            messages.success(
                request, f"¡Bienvenido {huesped.nombre} 👋 Tu cuenta fue creada con éxito!")

            return redirect("home")  # va al inicio con sesión iniciada
    else:
        form = HuespedForm()

    return render(request, "register.html", {"form": form})
