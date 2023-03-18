from os import stat
from django.urls import URLPattern, path
from . import views

from django.conf  import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('productos', views.productos, name='producto'),
    path('servicios', views.servicios, name='servicio'),
    path('registrar', views.crear_cuenta, name='crear-cuenta'),
    path('iniciar', views.iniciar_cuenta, name='iniciar-cuenta'),
    path('empleados', views.iniciar_empleados, name='iniciar-empleados'),
    path('cerrar', views.cerrar_cuenta, name='cerrar-cuenta'),

    path('suscripcion', views.suscribirme, name='suscripcion'),

    path('promociones', views.promos, name='promociones'),
    path('promo/<int:id>', views.agregar_promocion, name='promo'),

    path('historial', views.historial, name='historial'),
    path('mi-perfil', views.editar_perfil, name='perfil'),
    #-----### Zona de Compras ###-----#  
    path('carrito', views.carrito, name='carrito'),
    path('agregar-carrito/<int:id>', views.carrito_compras, name='agregar-carrito'),
    path('servicio-carrito/<int:id>', views.servicio_carrito, name='servicio-carrito'),

    path('add-carrito/<producto>', views.aumentar_carrito, name='aumentar-carrito'),
    path('remove-carrito/<producto>', views.descontar_carrito, name='descontar-carrito'),
    path('delete-carrito/<producto>', views.borrar_carrito, name='delete-carrito'),
    #-----### Zona de Recepción de Pagos ###-----#  
    path('cuenta-pagada', views.pagar, name='pagar'),

    path('promo-activa', views.activar_promocion, name='activar_promocion'),

    #-----### Zona Administrativa ###-----#                                                     Nivel Staff all
    path('administracion', views.admin, name='admin'),                                      

    #-----### Zona Administrativa Pedidos ###-----#                                             Nivel Staff 1
    path('pds-entregados', views.pedidos_entregados, name='pedidos-entregados'),
    path('pds-enviados', views.pedidos_enviados, name='pedidos-enviados'),
    path('pds-pendientes', views.pedidos_pendientes, name='pedidos-pendientes'),

    path('delete-pendientes/<int:id>', views.eliminar_pendientes, name='eliminar-pendientes'),
    path('delete-entregados/<int:id>', views.eliminar_entregados, name='eliminar-entregados'),
    path('delete-enviados/<int:id>', views.eliminar_enviados, name='eliminar-enviados'),
    path('edit-pendientes/<int:id>', views.editar_pedidos, name='editar-pedidos'),

    #-----### Zona Administrativa Bandeja ###-----#                                             Nivel Staff 2
    path('adm-bandeja', views.bandeja_admin, name='bandeja-admin'),    
    path('edit-bandeja/<int:id>', views.editar_bandeja, name='editar-bandeja'),
    path('delete-bandeja/<int:id>', views.eliminar_bandeja, name='eliminar-bandeja'),

    #-----### Zona Administrativa Productos/Servicios ###-----#                                 Nivel Staff 3
    path('adm-productos', views.productos_admin, name='productos-admin'),    
    path('crear-productos', views.crear_producto, name='crear-productos'),
    path('edit-productos/<int:id>', views.editar_productos, name='editar-productos'),
    path('delete-productos/<int:id>', views.eliminar_productos, name='eliminar-productos'),

    path('adm-servicios', views.servicios_admin, name='servicios-admin'),    
    path('crear-servicios', views.crear_servicios, name='crear-servicios'),
    path('edit-servicios/<int:id>', views.editar_servicios, name='editar-servicios'),
    path('delete-servicios/<int:id>', views.eliminar_servicios, name='eliminar-servicios'),
    
    #-----### Zona Administrativa Promociones ###-----#                                         Nivel Staff 4
    
    path('adm-promociones', views.promociones_admin, name='promociones-admin'),    
    path('crear-promociones', views.crear_promociones, name='crear-promociones'),
    path('edit-promociones/<int:id>', views.editar_promociones, name='editar-promociones'),
    path('delete-promociones/<int:id>', views.eliminar_promociones, name='eliminar-promociones'),
    
    #-----### Zona Administrativa Clientes/Staff ###-----#                                      Nivel Staff 5
    path('adm-clientes', views.clientes_admin, name='clientes-admin'),    
    path('crear-clientes', views.crear_clientes, name='crear-clientes'),
    path('edit-clientes/<int:id>', views.editar_clientes, name='editar-clientes'),
    path('delete-clientes/<int:id>', views.eliminar_clientes, name='eliminar-clientes'),


    path('adm-staff', views.staff_admin, name='staff-admin'),    
    path('crear-staff', views.crear_staff, name='crear-staff'),
    path('edit-staff/<int:id>', views.editar_staff, name='editar-staff'),
    path('delete-staff/<int:id>', views.eliminar_staff, name='eliminar-staff'),
    #-------------------------------------#

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)