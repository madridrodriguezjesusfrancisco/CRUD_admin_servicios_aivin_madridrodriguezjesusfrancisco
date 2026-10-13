
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from django.contrib.auth.decorators import login_required

from .models import Servicio
from .forms import ServicioForm


def inicio(request):
    info_bd = connection.settings_dict

    contexto = {
        'motor': info_bd['ENGINE'],
        'host': info_bd['HOST'],
    }

    return render(request, 'core/inicio.html', contexto)


def servicios(request):
    lista_servicios = Servicio.objects.all()

    return render(
        request,
        'core/servicios.html',
        {'servicios': lista_servicios}
    )


@login_required
def crear_servicio(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)

        if form.is_valid():
            nuevo = form.save(commit=False)
            nuevo.propietario = request.user
            nuevo.save()

            return redirect('servicios')
    else:
        form = ServicioForm()

    return render(
        request,
        'core/servicio_form.html',
        {'form': form, 'titulo_pagina': 'Nuevo servicio'}
    )


@login_required
def editar_servicio(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)

    if request.method == 'POST':
        form = ServicioForm(request.POST, instance=servicio)

        if form.is_valid():
            form.save()
            return redirect('servicios')
    else:
        form = ServicioForm(instance=servicio)

    return render(
        request,
        'core/servicio_form.html',
        {'form': form, 'titulo_pagina': 'Editar servicio'}
    )


@login_required
def eliminar_servicio(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)

    if request.method == 'POST':
        servicio.delete()
        return redirect('servicios')

    return render(
        request,
        'core/servicio_confirm_delete.html',
        {'servicio': servicio}
    )

# @login_required: solo usuarios con sesión iniciada pueden editar
@login_required
# pk: la clave primaria (id) que Django extrae del pedazo <int:pk> de la URL (paso 05)
def editar_servicio(request, pk):
    # busca el Servicio con ese id; si no existe, responde 404 automáticamente
    servicio = get_object_or_404(Servicio, pk=pk)
    # si el usuario envió el formulario con cambios, la petición llega como POST
    if request.method == 'POST':
        # instance=servicio: le dice al formulario "actualiza ESTE registro, no crees uno nuevo"
        form = ServicioForm(request.POST, instance=servicio)
        # is_valid(): revisa tipos de dato y campos obligatorios
        if form.is_valid():
            # save(): al tener instance=, guarda los cambios sobre el mismo registro (UPDATE, no INSERT)
            form.save()
            # redirect: regresa al listado después de guardar
            return redirect('servicios')
    # si no es POST, es GET: se acaba de abrir la pantalla de edición
    else:
        # instance=servicio sin datos de POST: precarga el formulario con los valores actuales
        form = ServicioForm(instance=servicio)
    # render: reutiliza servicio_form.html con el título "Editar servicio"
    return render(request, 'core/servicio_form.html', {'form': form, 'titulo_pagina': 'Editar servicio'})

# @login_required: solo usuarios con sesión iniciada pueden borrar
@login_required
# eliminar_servicio: recibe el pk (id) desde la URL /servicios/<pk>/eliminar/
def eliminar_servicio(request, pk):
    # busca el registro exacto a borrar, igual que en editar_servicio
    servicio = get_object_or_404(Servicio, pk=pk)
    # solo se borra si llega un POST (el botón de confirmar), nunca con un simple GET
    if request.method == 'POST':
        # delete(): borra la fila de MySQL de verdad
        servicio.delete()
        # redirect: regresa al listado, ya sin el registro borrado
        return redirect('servicios')
    # si es GET, solo muestra la pantalla de "¿Seguro?"; todavía no borra nada
    return render(request, 'core/servicio_confirm_delete.html', {'servicio': servicio})