from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Categoria, Producto
from .forms import CategoriaForm, ProductoForm
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.contrib import messages
from django.db.models import Count
from django.views.decorators.http import require_POST



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            error_msg = 'Por favor, completa todos los campos.'
            return render(request, 'tienda/login.html', {'error': error_msg})

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('listar_categorias')
        else:
            return render(request, 'tienda/login.html', {'error': 'Usuario o contraseña incorrectos'})

    return render(request, 'tienda/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')




@login_required
def listar_categorias(request):
    categorias = Categoria.objects.annotate(num_productos=Count('producto'))
    
    if request.method == 'POST':
        form = CategoriaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada con éxito.')
            return redirect('listar_categorias')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = CategoriaForm()
    
    return render(request, 'tienda/listar_categorias.html', {
        'categorias': categorias,
        'form': form,
    })


@login_required
def categoria_crear(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST, request.FILES)  # <-- aquí agregas request.FILES
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada con éxito')
            return redirect('listar_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'tienda/listar_categorias.html', {'form': form, 'categorias': Categoria.objects.all()})








@login_required
def categoria_editar(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)

    if request.method == 'POST':
        form = CategoriaForm(request.POST, request.FILES, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada con éxito.')
            return redirect('listar_categorias')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = CategoriaForm(instance=categoria)

    return render(request, 'tienda/categoria_editar.html', {
        'form': form,
        'categoria': categoria,
    })













@login_required
def productos_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    productos = Producto.objects.filter(categoria=categoria)
    
    generos = productos.values_list('genero__nombre', flat=True).distinct()
    generos = [g for g in generos if g]
    
    form = ProductoForm(initial={'categoria': categoria})

    return render(request, 'tienda/productos_por_categoria.html', {
        'categoria': categoria,
        'productos': productos,
        'generos': generos,
        'form': form,
    })

@login_required
def producto_crear(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.categoria = categoria  # Asignamos la categoría
            producto.save()
            messages.success(request, 'Producto agregado correctamente.')
            return redirect('productos_por_categoria', categoria_id=categoria.id)
    else:
        form = ProductoForm(initial={'categoria': categoria})

    return render(request, 'tienda/producto_crear_modal.html', {
        'form': form,
        'categoria': categoria
    })



def producto_editar(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('productos_por_categoria', categoria_id=producto.categoria.id)
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'tienda/producto_editar.html', {'form': form, 'producto': producto})


@login_required
@require_POST
def producto_eliminar(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    categoria_id = producto.categoria.id
    producto.delete()
    messages.success(request, 'Producto eliminado correctamente.')
    return redirect('productos_por_categoria', categoria_id=categoria_id)