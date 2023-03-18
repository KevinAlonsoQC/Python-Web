from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Clientes)
admin.site.register(Usuarios)
admin.site.register(Pedidos)
admin.site.register(Servicios)
admin.site.register(Productos)
admin.site.register(Bandeja)
admin.site.register(Promociones)
admin.site.register(Clientes_Promocionados)
admin.site.register(Carrito)