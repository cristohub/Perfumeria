from django import forms
from .models import Categoria, Producto

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'foto_destacada']  # agregamos el campo de la imagen
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la categoría'}),
            # Para la imagen no es necesario widget especial, pero puedes personalizar si quieres
        }

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        qs = Categoria.objects.filter(nombre__iexact=nombre)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe una categoría con ese nombre.")
        return nombre


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'categoria',       
            'nombre',
            'descripcion',
            'marca',
            'genero',
            'tipo_fragancia',
            'precio',
            'stock',
            'foto',
        ]
        widgets = {
        'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        'categoria': forms.HiddenInput(),
        'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        'marca': forms.Select(attrs={'class': 'form-select'}),
        'genero': forms.Select(attrs={'class': 'form-select'}),
        'tipo_fragancia': forms.Select(attrs={'class': 'form-select'}),
        'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
    }