from django.urls import path
from . import views


urlpatterns = [
  
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
     # Categorías
    path('categorias/', views.listar_categorias, name='listar_categorias'),
    path('categorias/crear/', views.categoria_crear, name='categoria_crear'),
    path('categorias/<int:categoria_id>/productos/', views.productos_por_categoria, name='productos_por_categoria'),
    path('categorias/<int:categoria_id>/productos/crear/', views.producto_crear, name='producto_crear'),
    path('categoria/editar/<int:categoria_id>/', views.categoria_editar, name='categoria_editar'),


    path('producto/<int:producto_id>/editar/', views.producto_editar, name='producto_editar'),

  path('producto/<int:producto_id>/eliminar/', views.producto_eliminar, name='producto_eliminar'),

]


