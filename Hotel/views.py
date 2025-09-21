from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .forms import HuespedForm


def home(request):
    return render(request, "home.html")


def login_view(request):
    return render(request, "login.html")


def register_view(request):
    if request.method == "POST":
        form = HuespedForm(request.POST)
        if form.is_valid():
            huesped = form.save(commit=False)  # no guarda todavía
            # se hashea en save()
            huesped.password = form.cleaned_data["password1"]
            huesped.save()
            return redirect("login")  # redirige al login tras registro exitoso
    else:
        form = HuespedForm()

    return render(request, "register.html", {"form": form})
