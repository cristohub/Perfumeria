import os
from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError

# Validador: solo permite imágenes .png
def validar_imagen_png(file):
    if not file.name.lower().endswith('.png'):
        raise ValidationError("Solo se permiten archivos PNG.")

# Función para personalizar el nombre del archivo
def nombre_foto_producto(instance, filename):
    nombre = slugify(instance.nombre)
    marca = slugify(instance.marca.nombre)
    extension = os.path.splitext(filename)[1]
    nuevo_nombre = f"{nombre}-{marca}{extension}"
    return os.path.join('productos', nuevo_nombre)




def validar_imagen_png_jpg(file):
    valid_extensions = ['.png', '.jpg', '.jpeg']
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError("Solo se permiten archivos PNG, JPG o JPEG.")

# MODELOS

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    foto_destacada = models.ImageField(
        upload_to='categorias/',
        blank=True,
        null=True,
        validators=[validar_imagen_png_jpg],
        help_text="Foto destacada para la categoría (PNG, JPG o JPEG)"
    )

    def __str__(self):
        return self.nombre

class Genero(models.Model):
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

class Marca(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    TIPO_FRAGANCIA_CHOICES = [
        ('citrico', 'Cítrico'),
        ('floral', 'Floral'),
        ('amaderado', 'Amaderado'),
        ('oriental', 'Oriental'),
        ('fresco', 'Fresco'),
        ('dulce', 'Dulce'),
        ('acuatico', 'Acuático'),
        # Puedes agregar más tipos si lo necesitas
    ]

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    tipo_fragancia = models.CharField(
        max_length=20,
        choices=TIPO_FRAGANCIA_CHOICES,
        blank=True,
        null=True,
        help_text="Solo aplica si es un perfume"
    )
    foto = models.ImageField(
        upload_to=nombre_foto_producto,
        blank=True,
        null=True,
        validators=[validar_imagen_png]
    )

    def __str__(self):
        return self.nombre
