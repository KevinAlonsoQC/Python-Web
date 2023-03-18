from distutils.command import upload
import email
from pyexpat import model
from django.db import models

class Clientes(models.Model):
    id = models.AutoField(primary_key=True)

    nombre_unico=models.CharField(unique=True, max_length=100, verbose_name='Nombre_Unico', null=False)

    nombre=models.CharField(max_length=40, verbose_name='Nombre', null=False)
    apellido=models.CharField(max_length=40, verbose_name='Apellido', null=False)
    email=models.EmailField(unique=True, max_length=100, verbose_name='Email', null=False)
    password=models.CharField(max_length=100, verbose_name='Contraseña', null=False)

    suscrito =models.BooleanField(verbose_name='Suscrito', null=False, default=False)
    sexo=models.CharField(max_length=1,verbose_name='Sexo', null=False)
    celular=models.CharField(max_length=9, verbose_name='Celular', null=False)
    edad=models.IntegerField(verbose_name='Edad', null=False)

    pais=models.CharField(max_length=50,verbose_name='País', null=False)
    ciudad=models.CharField(max_length=50, verbose_name='Ciudad', null=False)
    comuna=models.CharField(max_length=50, verbose_name='Comuna', null=False)

    def __str__(self):
        fila = "ID: " + str(self.id) + " | Nombre Único: " + self.nombre_unico + " | Nombre: " + self.nombre + " | Apellido: " + self.apellido + " | Email: " + self.email
        return fila


class Usuarios(models.Model):
    id = models.AutoField(primary_key=True)

    nombre_unico=models.CharField(unique=True, max_length=100, verbose_name='Nombre_Unico', null=False)

    nombre=models.CharField(max_length=40, verbose_name='Nombre', null=False)
    apellido=models.CharField(max_length=40, verbose_name='Apellido', null=False)
    email=models.EmailField(unique=True, max_length=100, verbose_name='Email', null=False)
    password=models.CharField(max_length=100, verbose_name='Contraseña', null=False)

    sexo=models.CharField(max_length=1,verbose_name='Sexo', null=False)
    celular=models.CharField(max_length=9, verbose_name='Celular', null=False)
    edad=models.IntegerField(verbose_name='Edad', null=False)

    nivel_staff=models.IntegerField(verbose_name='Nivel Staff', null=True, default=0)

    def __str__(self):
        fila = "ID: " + str(self.id) + " | Nombre Único: " + self.nombre_unico + " | Nombre: " + self.nombre + " | Apellido: " + self.apellido + " | Email: " + self.email + " | Nivel Staff: " + str(self.nivel_staff)
        return fila   

class Pedidos(models.Model):
    id = models.AutoField(primary_key=True)
    
    cliente=models.CharField(max_length=100, verbose_name='Nombre_Unico', null=False)
    producto=models.TextField(verbose_name='Producto', null=False)
    fecha_pedido=models.DateField(verbose_name='Fecha Pedido', null=False)
    fecha_entrega=models.DateField(verbose_name='Fecha Entrega', null=True, default=0)
    total=models.IntegerField(verbose_name='Monto_Pagado', null=False)
    prioridad=models.IntegerField(verbose_name='Prioridad', null=False, default=0)
    numero_seguimiento=models.CharField(max_length=100,verbose_name='Número de Seguimiento', null=True)
    estado=models.CharField(max_length=100, verbose_name='Estado Pedido', null=False, default='Preparando')
    calle_envio=models.CharField(max_length=100, verbose_name='Calle de Envio', null=False, default='nulo')
    comuna_envio=models.CharField(max_length=100, verbose_name='Comuna de Envio', null=False, default='nulo')
    ciudad_envio=models.CharField(max_length=100, verbose_name='Ciudad de Envio', null=False, default='nulo')

    def __str__(self):
        fila = "ID: " + str(self.id) + " | Cliente: " + self.cliente + " | Fecha Pedido: " + str(self.fecha_pedido)  + " | Fecha Entrega: " + str(self.fecha_entrega) + " | Total: " + str(self.total) + " | Prioridad: " + str(self.prioridad) + " | Estado: " + self.estado
        return fila

class Servicios(models.Model):
    id = models.AutoField(primary_key=True)
    
    producto=models.CharField(max_length=100, verbose_name='Producto', null=False)
    descripcion=models.TextField(verbose_name='Descripcion', null=True)

    precio=models.IntegerField(verbose_name='Precio', null=False)
    imagen = models.ImageField(upload_to='imagenes/', verbose_name='Imagen',null=False)

    def __str__(self):
        fila = "ID: " + str(self.id) + " | Producto: " + self.producto + " | Precio: " + str(self.precio)
        return fila
    
    def delete(self, using=None, keep_parents=False):
        self.imagen.storage.delete(self.imagen.name)
        super().delete()

class Productos(models.Model):
    id = models.AutoField(primary_key=True)
    
    producto=models.CharField(max_length=100, verbose_name='Producto', null=False)
    descripcion=models.TextField(verbose_name='Descripcion', null=True)

    precio=models.IntegerField(verbose_name='Precio', null=False)
    stock=models.IntegerField(verbose_name='Stock_Disponible', null=False)
    imagen = models.ImageField(upload_to='imagenes/', verbose_name='Imagen', null=False)

    def __str__(self):
        fila = "ID: " + str(self.id) + " | Producto: " + self.producto + " | Precio: " + str(self.precio) + " | Stock: " + str(self.stock)
        return fila

    def delete(self, using=None, keep_parents=False):
        self.imagen.storage.delete(self.imagen.name)
        super().delete()
    

class Bandeja(models.Model):
    id = models.AutoField(primary_key=True)
    
    email=models.EmailField(max_length=100, verbose_name='Email', null=False)
    nombre=models.CharField(max_length=40, verbose_name='Nombre', null=False)
    apellido=models.CharField(max_length=40, verbose_name='Apellido', null=False)
    tipo=models.CharField(max_length=40,verbose_name='Tipo', null=False)
    fecha=models.DateField(verbose_name='Fecha', null=False)
    descripcion=models.TextField(verbose_name='Descripcion', null=True)
    leido=models.BooleanField(verbose_name='Visto', null=False, default=False)

    def __str__(self):
        fila = "ID: " + str(self.id) + " | Email: " + self.email + " | Nombre: " + str(self.nombre) + " | Apellido: " + str(self.apellido) + " | Tipo: " + str(self.tipo) + " | Fecha: " + str(self.fecha)
        return fila 

class Promociones(models.Model):
    id = models.AutoField(primary_key=True)
    
    nombre=models.CharField(max_length=40, verbose_name='Nombre Promoción', null=False)
    fecha_inicio=models.DateField(verbose_name='Fecha Inicio', null=False)
    fecha_fin=models.DateField(verbose_name='Fecha Fin', null=False)
    porcentaje_descuento=models.IntegerField(verbose_name='Porcentaje de Descuento', null=False, default=0)
    descripcion=models.TextField(verbose_name='Descripcion', null=True)

    def __str__(self):
        fila = "ID: " + str(self.id) + " | Nombre Promoción: " + self.nombre + " | Fecha Inicial: " + str(self.fecha_inicio) + " | Fecha Final: " + str(self.fecha_fin) + " | Descuento %: " + str(self.porcentaje_descuento)
        return fila 

class Clientes_Promocionados(models.Model):
    id = models.AutoField(primary_key=True)
    
    cliente=models.CharField(max_length=100, verbose_name='Nombre_Unico', null=False)
    vencimiento=models.DateField(verbose_name='Vencimiento', null=False)
    porcentaje_descuento=models.IntegerField(verbose_name='Porcentaje de Descuento', null=False, default=0)
    promocion=models.IntegerField(verbose_name='ID de la promocion', null=False, default=0)
    promocion_name=models.TextField(verbose_name='Nombre de la promocion', null=False, default='Promoción')

    def __str__(self):
        fila = "ID: " + str(self.id) + " | Cliente: " + self.cliente + " | vencimiento: " + str(self.vencimiento) + " | Descuento %: " + str(self.porcentaje_descuento) + " | Nombre Promoción: " + str(self.promocion)
        return fila 

class Carrito(models.Model):
    id = models.AutoField(primary_key=True)
    
    producto=models.CharField(max_length=100, verbose_name='Producto', null=False)
    cantidad=models.IntegerField(verbose_name='Cantidad', null=False)
    precio_unitario=models.IntegerField(verbose_name='Precio Unitario', null=False)
    total=models.IntegerField(verbose_name='Total', null=False)

    def __str__(self):
        fila = "ID: " + str(self.id) + " | Producto: " + self.producto + " | Cantidad: " + str(self.cantidad) + " | Precio Unidad: " + str(self.precio_unitario) + " | Total: " + str(self.total)
        return fila