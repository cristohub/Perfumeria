from django.contrib import admin
from .models import Categoria, Genero, Marca, Producto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca', 'categoria', 'genero', 'precio', 'stock', 'tipo_fragancia')
    list_filter = ('marca', 'categoria', 'genero', 'tipo_fragancia')
    search_fields = ('nombre', 'descripcion')
