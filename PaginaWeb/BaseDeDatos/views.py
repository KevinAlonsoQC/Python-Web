from hashlib import new
from re import S
import re
from django.shortcuts import render, redirect
from django.http import HttpResponse
from pymysql import NULL
from .models import *
from random import randint
from django.contrib import messages
from .forms import *
from datetime import datetime, date, timedelta
import time


inLogin = False
cliente_unico = ''
nombre = ''
apellido = ''
correo = ''
sexo = ''
nivel_staff = 0
suscrito = False

calle_envio = ''
comuna_envio = ''
ciudad_envio = ''

carro = []


# Create your views here.
def inicio(request):
    global inLogin
    global nombre
    global apellido
    global sexo
    global correo
    global cliente_unico
    global nivel_staff

    if request.method == 'POST':       
    
        emailContacto=request.POST['emailContacto']
        nombreContacto=request.POST['nombreContacto']
        apellidoContacto=request.POST['apellidoContacto']
        tipoContacto=request.POST['tipoContacto']
        descContacto=request.POST['descContacto']
        
        Bandeja(
                email=emailContacto,
                nombre=nombreContacto,
                apellido=apellidoContacto,
                tipo=tipoContacto,
                fecha=date.today().strftime('%Y-%m-%d'),
                descripcion=descContacto,
            ).save()
        
    return render(request,"index.html", {'sesion': inLogin, 'nombre':nombre, 'apellido':apellido, 'sexo':sexo, 'correo':correo, 'staff':nivel_staff})

def editar_perfil(request):
    global inLogin
    global nombre
    global apellido
    global sexo
    global correo
    global nivel_staff
    global cliente_unico

    newCorreo = request.GET.get("newCorreo")
    newCorreRep = request.GET.get("newCorreoRep")

    newPass = request.GET.get("newPass")
    newPassRep = request.GET.get("newPassRep")

    if newCorreo and newCorreRep:
        if newCorreo == newCorreRep:
            cliente = Clientes.objects.all()
            for v in cliente:
                if v.nombre_unico == cliente_unico:
                    v.email = newCorreo
                    v.save()
                    return redirect('cerrar-cuenta')
        else:
             messages.success(request, '¡Los correos no coinciden!')

    if newPass and newPassRep:
        if newPass == newPassRep:
            cliente = Clientes.objects.all()
            for v in cliente:
                if v.nombre_unico == cliente_unico:
                    v.password = newPass
                    v.save()
                    return redirect('cerrar-cuenta')
        else:
             messages.success(request, '¡Los contraseñas no coinciden!')

    if request.method == 'POST':
        cliente = Clientes.objects.all()

        for v in cliente:
            if v.nombre_unico == cliente_unico:
                v.nombre = request.POST['nameEdit']
                v.apellido = request.POST['apellidoEdit']
                v.celular = request.POST['celularEdit']
                v.pais = request.POST['paisEdit']
                v.ciudad = request.POST['ciudadEdit']
                v.comuna = request.POST['comunaEdit']
                v.save()
                return redirect('cerrar-cuenta')


    return render(request, "usuarios/editar_perfil.html", {'sesion': inLogin, 'nombre':nombre, 'apellido':apellido, 'sexo':sexo, 'correo':correo, 'staff':nivel_staff})

def promos(request):
    global inLogin
    global nombre
    global apellido
    global sexo
    global correo
    global nivel_staff

    global cliente_unico

    promo_list = []
    promociones = Promociones.objects.all()
    for v in promociones:
        fecha_hoy = datetime.now().date()
        fecha_inicial = datetime.strptime(str(v.fecha_inicio), '%Y-%m-%d')
        if str(fecha_inicial) <= str(fecha_hoy):
            prom = {
                'id': v.id,
                'nombre':v.nombre,
                'descripcion': v.descripcion,
                'fecha_inicio':v.fecha_inicio,
                'fecha_fin':v.fecha_fin,
                'porcentaje_descuento':v.porcentaje_descuento,
            }
            promo_list.append(prom)


    return render(request,"promociones/promociones.html",{'sesion': inLogin, 'nombre':nombre, 'apellido':apellido, 'sexo':sexo, 'correo':correo, 'staff':nivel_staff, 'promos':promo_list} )

def historial(request):
    global inLogin
    global nombre
    global apellido
    global sexo
    global correo
    global nivel_staff

    global cliente_unico

    pedidos = Pedidos.objects.filter(cliente=cliente_unico)
    return render(request,"pedidos/historial.html", {'historial':pedidos, 'sesion': inLogin, 'nombre':nombre, 'apellido':apellido, 'sexo':sexo, 'correo':correo, 'staff':nivel_staff} )

def productos(request):
    global inLogin
    global nombre
    global apellido
    global sexo
    global correo
    global nivel_staff
    global suscrito

    buscador = request.GET.get("b_prd")
    producto = Productos.objects.all()
    
    if suscrito:
        productos_dsct = []
        for v in producto:
            dsct = {
                    'id': v.id,
                    'producto': v.producto,
                    'descripcion': v.descripcion,
                    'precio': int(v.precio-((v.precio*5)//100)),
                    'stock': v.stock,
                    'precio_an': v.precio,
                    'imagen': v.imagen,
                }
            productos_dsct.append(dsct)
        return render(request,"productos/productos.html", { 'productos':productos_dsct, 'sesion': inLogin, 'nombre':nombre, 'apellido':apellido, 'sexo':sexo, 'correo':correo, 'staff':nivel_staff , 'suscrito':suscrito} )

    if buscador:
        producto = Productos.objects.filter(producto__icontains=buscador)
        if suscrito:
            productos_dsct = []
            for v in producto:
                dsct = {
                        'id': v.id,
                        'producto': v.producto,
                        'descripcion': v.descripcion,
                        'precio': int(v.precio-((v.precio*5)//100)),
                        'stock': v.stock,
                        'precio_an': v.precio,
                        'imagen': v.imagen,
                    }
                productos_dsct.append(dsct)
            return render(request,"productos/productos.html", { 'productos':productos_dsct, 'sesion': inLogin, 'nombre':nombre, 'apellido':apellido, 'sexo':sexo, 'correo':correo, 'staff':nivel_staff , 'suscrito':suscrito} )
    

    return render(request,"productos/productos.html", { 'productos':producto, 'sesion': inLogin, 'nombre':nombre, 'apellido':apellido, 'sexo':sexo, 'correo':correo, 'staff':nivel_staff , 'suscrito':suscrito} )


def servicios(request):
    global inLogin
    global nombre
    global apellido
    global sexo
    global correo
    global nivel_staff
    global suscrito

    buscador = request.GET.get("b_srv")
    producto = Servicios.objects.all()

    if buscador:
        producto = Servicios.objects.filter(producto__icontains=buscador)

    return render(request,"servicios/servicios.html", { 'productos':producto , 'sesion': inLogin, 'nombre':nombre, 'apellido':apellido, 'sexo':sexo, 'correo':correo, 'staff':nivel_staff, 'suscrito':suscrito} )

def crear_cuenta(request):
    global inLogin

    noProblem = True
    formulario = UsuariosForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':       
             
        nombre=request.POST['nombre']
        apellido=request.POST['apellido']
        email=request.POST['email']
        password=request.POST['password']

        sexo=request.POST['sexo']

        celular=request.POST['celular']
        edad=request.POST['edad']

        pais=request.POST['pais']
        ciudad=request.POST['ciudad']
        comuna=request.POST['comuna']

        fisrtRandom = randint(1000, 9999)
        secondRandom = randint(100, 999)
        resultado = str(fisrtRandom+secondRandom)

        nombre_unico = nombre[0:2]+resultado+apellido[0:2]

        while Clientes.objects.filter(nombre_unico=nombre_unico):
            fisrtRandom = randint(1000, 9999)
            secondRandom = randint(100, 999)
            resultado = str(fisrtRandom+secondRandom)

            nombre_unico = nombre[0:2]+resultado+apellido[0:2]

        if Clientes.objects.filter(email=email):
            noProblem = False
            messages.warning(request, '¡Este correo ya está en uso!')

        if len(password) < 6:
            noProblem = False
            messages.warning(request, '¡La contraseña debe tener al menos 6 dígitos!')
 

        if noProblem:
            Clientes(
                nombre_unico=nombre_unico,
                nombre=nombre,
                apellido=apellido,
                email=email,
                password=password,

                sexo=sexo,
                celular=celular,
                edad=edad,

                pais=pais,
                ciudad=ciudad,
                comuna=comuna
            ).save()
            messages.success(request, 'El usuario: '+nombre+' '+apellido+' ha sido registrado con éxito.')
            return render(request,"index.html", {'creada': True, 'sesion': inLogin})

    return render(request,"usuarios/crear_cuenta.html", {'formulario':formulario, 'sesion': inLogin})

def iniciar_cuenta(request):
    global inLogin
    global nombre
    global apellido
    global sexo
    global correo
    global nivel_staff
    global cliente_unico
    global suscrito

    noProblem = False

    if request.method == 'POST':       
    
        email=request.POST['emailUser']
        password=request.POST['passwordUser']

        clientes = Clientes.objects.all()
        for v in clientes:
            if v.email == email:
                if v.password == password:
                    noProblem = True
                    if noProblem:
                        inLogin = True
                        nombre = v.nombre
                        apellido = v.apellido
                        sexo = v.sexo
                        correo = v.email
                        cliente_unico = v.nombre_unico
                        suscrito = v.suscrito
                        return render(request,"index.html", {'sesion': inLogin, 'nombre':nombre, 'apellido':apellido, 'sexo':sexo, 'correo':correo, 'staff':nivel_staff})
                    else:
                        messages.warning(request, '¡Email o Contraseña incorrecta!')
                        return render(request,"usuarios/iniciar_sesion.html", {'sesion': inLogin, 'nombre':nombre, 'apellido':apellido, 'sexo':sexo, 'correo':correo, 'staff':nivel_staff})


    return render(request,"usuarios/iniciar_sesion.html")

def iniciar_empleados(request):
    global inLogin
    global nombre
    global apellido
    global sexo
    global correo
    global nivel_staff
    noProblem = False

    if request.method == 'POST':       
    
        email=request.POST['emailUser']
        password=request.POST['passwordUser']

        clientes = Usuarios.objects.all()
        for v in clientes:
            if v.email == email:
                if v.password == password:
                    noProblem = True
                    if noProblem:
                        inLogin = True
                        nombre = v.nombre
                        apellido = v.apellido
                        sexo = v.sexo
                        correo = v.email
                        nivel_staff = v.nivel_staff
                        return render(request,"index.html", {'sesion': inLogin, 'nombre':nombre, 'apellido':apellido, 'sexo':sexo, 'correo':correo, 'staff':nivel_staff})
                    else:
                        messages.warning(request, '¡Email o Contraseña incorrecta!')
                        return render(request,"usuarios/iniciar_empleados.html", {'sesion': inLogin, 'nombre':nombre, 'apellido':apellido, 'sexo':sexo, 'correo':correo, 'staff':nivel_staff})


    return render(request,"usuarios/iniciar_empleados.html")

def cerrar_cuenta(request):
    global inLogin
    global nombre
    global apellido
    global sexo
    global correo
    global nivel_staff
    global cliente_unico


    inLogin = False
    nombre = ''
    apellido = ''
    sexo = ''
    correo = ''
    nivel_staff = 0
    cliente_unico = ''

    
    return render(request,"index.html", {'sesion': inLogin, 'nombre':nombre, 'apellido':apellido, 'sexo':sexo, 'correo':correo, 'staff':nivel_staff})




def admin(request):
    global inLogin
    global nombre
    global apellido
    global sexo
    global correo
    global nivel_staff
    
    return render(request,"administracion/admin.html", {'sesion': inLogin, 'nombre':nombre, 'apellido':apellido, 'sexo':sexo, 'correo':correo, 'staff':nivel_staff})

def pedidos_enviados(request):
    global inLogin
    global nombre
    global apellido
    global sexo
    global correo
    global nivel_staff


    buscador = request.GET.get("b_pedido_enviados")
    pedidos = Pedidos.objects.filter(estado='Enviado')

    if buscador:
        pedidos = Pedidos.objects.filter(numero_seguimiento__icontains=buscador, estado='Enviado')


    return render(request,"administracion/pedidos/admin_pedidos_en.html", 
        {
            'sesion': inLogin, 
            'nombre':nombre, 
            'apellido':apellido, 
            'sexo':sexo, 
            'correo':correo, 
            'staff':nivel_staff,
            'pedidos': pedidos
        })

def pedidos_entregados(request):
    global inLogin
    global nombre
    global apellido
    global sexo
    global correo
    global nivel_staff


    buscador = request.GET.get("b_pedido_entregado")
    pedidos = Pedidos.objects.filter(estado='Entregado')

    if buscador:
        pedidos = Pedidos.objects.filter(numero_seguimiento__icontains=buscador, estado='Entregado')


    return render(request,"administracion/pedidos/admin_pedidos_e.html", 
        {
            'sesion': inLogin, 
            'nombre':nombre, 
            'apellido':apellido, 
            'sexo':sexo, 
            'correo':correo, 
            'staff':nivel_staff,
            'pedidos': pedidos
        })

def pedidos_pendientes(request):
    global inLogin
    global nombre
    global apellido
    global sexo
    global correo
    global nivel_staff


    buscador = request.GET.get("b_pedido_pendiente")
    pedidos = Pedidos.objects.filter(estado='Preparando')

    if buscador:
        pedidos = Pedidos.objects.filter(numero_seguimiento__icontains=buscador, estado='Preparando')


    return render(request,"administracion/pedidos/admin_pedidos_p.html", 
        {
            'sesion': inLogin, 
            'nombre':nombre, 
            'apellido':apellido, 
            'sexo':sexo, 
            'correo':correo, 
            'staff':nivel_staff,
            'pedidos': pedidos
        })


def editar_pedidos(request, id):
    global inLogin
    global nombre
    global apellido
    global sexo
    global correo
    global nivel_staff

    pendiente = Pedidos.objects.get(id=id)
    formulario = PedidosForm(request.POST or None, request.FILES or None, instance=pendiente)
    
    if request.method == 'POST':
        pendiente.delete()
        Pedidos(
                cliente=request.POST['cliente'],
                producto=request.POST['producto'],
                fecha_pedido=request.POST['fecha_pedido'],
                fecha_entrega=request.POST['fecha_entrega'],
                total=request.POST['total'],
                prioridad=request.POST['prioridad'],
                numero_seguimiento=request.POST['numero_seguimiento'],
                estado=request.POST['estado'],
                calle_envio=request.POST['calle_envio'],
                comuna_envio=request.POST['comuna_envio'],
                ciudad_envio=request.POST['ciudad_envio'],

        ).save()
        return redirect("pedidos-pendientes")


    return render(request,"administracion/pedidos/admin_pedidos_editar.html", 
        {
            'sesion': inLogin, 
            'nombre':nombre, 
            'apellido':apellido, 
            'sexo':sexo, 
            'correo':correo, 
            'staff':nivel_staff,
            'formulario':formulario,
        })





def eliminar_pendientes(request, id):
    pendiente = Pedidos.objects.get(id=id)
    pendiente.delete()

    messages.warning(request, '¡Haz eliminado el pedido pendiente con ID: '+ str(id) +'!')
    return redirect('pedidos-pendientes')

def eliminar_enviados(request, id):
    enviado = Pedidos.objects.get(id=id)
    enviado.delete()

    messages.warning(request, '¡Haz eliminado el pedido enviado con ID: '+ str(id) +'!')
    return redirect('pedidos-enviados')

def eliminar_entregados(request, id):
    entregado = Pedidos.objects.get(id=id)
    entregado.delete()

    messages.warning(request, '¡Haz eliminado el pedido entregado con ID: '+ str(id) +'!')
    return redirect('pedidos-entregados')


def productos_admin(request):
    global inLogin
    global nombre
    global apellido
    global sexo
    global correo
    global nivel_staff


    buscador = request.GET.get("b_productos")
    productos = Productos.objects.all()

    if buscador:
        productos = Productos.objects.filter(producto__icontains=buscador)


    return render(request,"administracion/productos/productos_admin.html", 
        {
            'sesion': inLogin, 
            'nombre':nombre, 
            'apellido':apellido, 
            'sexo':sexo, 
            'correo':correo, 
            'staff':nivel_staff,
            'pedidos': productos
        })

def crear_producto(request):
    global inLogin
    global nombre
    global apellido
    global sexo
    global correo
    global nivel_staff

    formulario = ProductosForm(request.POST or None, request.FILES or None)

    if formulario.is_valid():       
        formulario.save()
        
        messages.success(request, 'El producto ha sido creado con éxito.')
        return redirect("productos-admin")

    return render(request,"administracion/productos/productos_crear.html", 
        {
            'sesion': inLogin, 
            'nombre':nombre, 
            'apellido':apellido, 
            'sexo':sexo, 
            'correo':correo, 
            'staff':nivel_staff,
            'formulario':formulario,
        })

def editar_productos(request, id):
    global inLogin
    global nombre
    global apellido
    global sexo
    global correo
    global nivel_staff

    pendiente = Productos.objects.get(id=id)
    formulario = ProductosForm(request.POST or None, request.FILES or None, instance=pendiente)
    
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect("productos-admin")


    return render(request,"administracion/productos/productos_editar.html", 
        {
            'sesion': inLogin, 
            'nombre':nombre, 
            'apellido':apellido, 
            'sexo':sexo, 
            'correo':correo, 
            'staff':nivel_staff,
            'formulario':formulario,
        })

def eliminar_productos(request, id):
    prod = Productos.objects.get(id=id)
    prod.delete()

    messages.warning(request, '¡Haz eliminado el Producto con ID: '+ str(id) +'!')
    return redirect('productos-admin')

######################################################################

def servicios_admin(request):
    global inLogin
    global nombre
    global apellido
    global sexo
    global correo
    global nivel_staff


    buscador = request.GET.get("b_servicios")
    servicios = Servicios.objects.all()

    if buscador:
        servicios = Servicios.objects.filter(producto__icontains=buscador)


    return render(request,"administracion/servicios/servicios_admin.html", 
        {
            'sesion': inLogin, 
            'nombre':nombre, 
            'apellido':apellido, 
            'sexo':sexo, 
            'correo':correo, 
            'staff':nivel_staff,
            'pedidos': servicios
        })

def crear_servicios(request):
    global inLogin
    global nombre
    global apellido
    global sexo
    global correo
    global nivel_staff

    formulario = ServiciosForm(request.POST or None, request.FILES or None)

    if formulario.is_valid():       
        formulario.save()
        
        messages.success(request, 'El servicio ha sido creado con éxito.')
        return redirect("servicios-admin")

    return render(request,"administracion/servicios/servicios_crear.html", 
        {
            'sesion': inLogin, 
            'nombre':nombre, 
            'apellido':apellido, 
            'sexo':sexo, 
            'correo':correo, 
            'staff':nivel_staff,
            'formulario':formulario,
        })

def editar_servicios(request, id):
    global inLogin
    global nombre
    global apellido
    global sexo
    global correo
    global nivel_staff

    pendiente = Servicios.objects.get(id=id)
    formulario = ServiciosForm(request.POST or None, request.FILES or None, instance=pendiente)
    
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect("servicios-admin")


    return render(request,"administracion/servicios/servicios_editar.html", 
        {
            'sesion': inLogin, 
            'nombre':nombre, 
            'apellido':apellido, 
            'sexo':sexo, 
            'correo':correo, 
            'staff':nivel_staff,
            'formulario':formulario,
        })

def eliminar_servicios(request, id):
    prod = Servicios.objects.get(id=id)
    prod.delete()

    messages.warning(request, '¡Haz eliminado el servicio con ID: '+ str(id) +'!')
    return redirect('servicios-admin')

######################################################################
######################################################################

def promociones_admin(request):
    global inLogin
    global nombre
    global apellido
    global sexo
    global correo
    global nivel_staff


    buscador = request.GET.get("b_promociones")
    promos = Promociones.objects.all()

    if buscador:
        promos = Promociones.objects.filter(nombre__icontains=buscador)


    return render(request,"administracion/promociones/promociones_admin.html", 
        {
            'sesion': inLogin, 
            'nombre':nombre, 
            'apellido':apellido, 
            'sexo':sexo, 
            'correo':correo, 
            'staff':nivel_staff,
            'pedidos': promos
        })

def crear_promociones(request):
    global inLogin
    global nombre
    global apellido
    global sexo
    global correo
    global nivel_staff

    formulario = PromocionesForm(request.POST or None, request.FILES or None)

    if formulario.is_valid():       
        formulario.save()
        
        messages.success(request, 'La promoción ha sido creado con éxito.')
        return redirect("promociones-admin")

    return render(request,"administracion/promociones/promociones_crear.html", 
        {
            'sesion': inLogin, 
            'nombre':nombre, 
            'apellido':apellido, 
            'sexo':sexo, 
            'correo':correo, 
            'staff':nivel_staff,
            'formulario':formulario,
        })

def editar_promociones(request, id):
    global inLogin
    global nombre
    global apellido
    global sexo
    global correo
    global nivel_staff

    pendiente = Promociones.objects.get(id=id)
    formulario = PromocionesForm(request.POST or None, request.FILES or None, instance=pendiente)
    
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect("promociones-admin")


    return render(request,"administracion/promociones/promociones_editar.html", 
        {
            'sesion': inLogin, 
            'nombre':nombre, 
            'apellido':apellido, 
            'sexo':sexo, 
            'correo':correo, 
            'staff':nivel_staff,
            'formulario':formulario,
        })

def eliminar_promociones(request, id):
    prod = Promociones.objects.get(id=id)
    prod.delete()

    messages.warning(request, '¡Haz eliminado la promoción con ID: '+ str(id) +'!')
    return redirect('promociones-admin')


######################################################################


def clientes_admin(request):
    global inLogin
    global nombre
    global apellido
    global sexo
    global correo
    global nivel_staff


    buscador = request.GET.get("b_usuarios")
    promos = Clientes.objects.all()

    if buscador:
        promos = Clientes.objects.filter(nombre_unico__icontains=buscador)


    return render(request,"administracion/clientes/clientes_admin.html", 
        {
            'sesion': inLogin, 
            'nombre':nombre, 
            'apellido':apellido, 
            'sexo':sexo, 
            'correo':correo, 
            'staff':nivel_staff,
            'pedidos': promos
        })

def crear_clientes(request):
    global inLogin
    global nombre
    global apellido
    global sexo
    global correo
    global nivel_staff

    noProblem = True

    formulario = UsuariosForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':       
             
        nombre=request.POST['nombre']
        apellido=request.POST['apellido']
        email=request.POST['email']
        password=request.POST['password']

        sexo=request.POST['sexo']

        celular=request.POST['celular']
        edad=request.POST['edad']

        pais=request.POST['pais']
        ciudad=request.POST['ciudad']
        comuna=request.POST['comuna']

        fisrtRandom = randint(1000, 9999)
        secondRandom = randint(100, 999)
        resultado = str(fisrtRandom+secondRandom)

        nombre_unico = nombre[0:2]+resultado+apellido[0:2]

        while Clientes.objects.filter(nombre_unico=nombre_unico):
            fisrtRandom = randint(1000, 9999)
            secondRandom = randint(100, 999)
            resultado = str(fisrtRandom+secondRandom)

            nombre_unico = nombre[0:2]+resultado+apellido[0:2]

        if Clientes.objects.filter(email=email):
            noProblem = False
            messages.warning(request, '¡Este correo ya está en uso!')

        if len(password) < 6:
            noProblem = False
            messages.warning(request, '¡La contraseña debe tener al menos 6 dígitos!')
 

        if noProblem:
            Clientes(
                nombre_unico=nombre_unico,
                nombre=nombre,
                apellido=apellido,
                email=email,
                password=password,

                sexo=sexo,
                celular=celular,
                edad=edad,

                pais=pais,
                ciudad=ciudad,
                comuna=comuna
            ).save()
            messages.success(request, 'El usuario: '+nombre+' '+apellido+' ha sido registrado con éxito.')
            return redirect("clientes-admin")

    return render(request,"administracion/clientes/clientes_crear.html", 
        {
            'sesion': inLogin, 
            'nombre':nombre, 
            'apellido':apellido, 
            'sexo':sexo, 
            'correo':correo, 
            'staff':nivel_staff,
            'formulario':formulario,
        })

def editar_clientes(request, id):
    global inLogin
    global nombre
    global apellido
    global sexo
    global correo
    global nivel_staff

    pendiente = Clientes.objects.get(id=id)
    formulario = UsuariosForm(request.POST or None, request.FILES or None, instance=pendiente)
    
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect("clientes-admin")


    return render(request,"administracion/clientes/clientes_editar.html", 
        {
            'sesion': inLogin, 
            'nombre':nombre, 
            'apellido':apellido, 
            'sexo':sexo, 
            'correo':correo, 
            'staff':nivel_staff,
            'formulario':formulario,
        })

def eliminar_clientes(request, id):
    prod = Clientes.objects.get(id=id)
    prod.delete()

    messages.warning(request, '¡Haz eliminado la cliente con ID: '+ str(id) +'!')
    return redirect('clientes-admin')


######################################################################

def staff_admin(request):
    global inLogin
    global nombre
    global apellido
    global sexo
    global correo
    global nivel_staff


    buscador = request.GET.get("b_staff")
    promos = Usuarios.objects.all()

    if buscador:
        promos = Usuarios.objects.filter(nombre_unico__icontains=buscador)


    return render(request,"administracion/staff/staff_admin.html", 
        {
            'sesion': inLogin, 
            'nombre':nombre, 
            'apellido':apellido, 
            'sexo':sexo, 
            'correo':correo, 
            'staff':nivel_staff,
            'pedidos': promos
        })

def crear_staff(request):
    global inLogin
    global nombre
    global apellido
    global sexo
    global correo
    global nivel_staff

    noProblem = True

    formulario = StaffForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':       
             
        nombre=request.POST['nombre']
        apellido=request.POST['apellido']
        email=request.POST['email']
        password=request.POST['password']

        sexo=request.POST['sexo']
        celular=request.POST['celular']
        edad=request.POST['edad']
        nivel_admin=request.POST['nivel_staff']

        fisrtRandom = randint(1000, 9999)
        secondRandom = randint(100, 999)
        resultado = str(fisrtRandom+secondRandom)

        nombre_unico = nombre[0:2]+resultado+apellido[0:2]

        while Usuarios.objects.filter(nombre_unico=nombre_unico):
            fisrtRandom = randint(1000, 9999)
            secondRandom = randint(100, 999)
            resultado = str(fisrtRandom+secondRandom)

            nombre_unico = nombre[0:2]+resultado+apellido[0:2]

        if Usuarios.objects.filter(email=email):
            noProblem = False
            messages.warning(request, '¡Este correo ya está en uso!')

        if len(password) < 6:
            noProblem = False
            messages.warning(request, '¡La contraseña debe tener al menos 6 dígitos!')
 

        if noProblem:
            Usuarios(
                nombre_unico=nombre_unico,
                nombre=nombre,
                apellido=apellido,
                email=email,
                password=password,

                sexo=sexo,
                celular=celular,
                edad=edad,
                nivel_staff=nivel_admin,
            ).save()
            messages.success(request, 'El staff: '+nombre+' '+apellido+' ha sido registrado con éxito.')
            return redirect("staff-admin")

    return render(request,"administracion/staff/staff_crear.html", 
        {
            'sesion': inLogin, 
            'nombre':nombre, 
            'apellido':apellido, 
            'sexo':sexo, 
            'correo':correo, 
            'staff':nivel_staff,
            'formulario':formulario,
        })

def editar_staff(request, id):
    global inLogin
    global nombre
    global apellido
    global sexo
    global correo
    global nivel_staff

    pendiente = Usuarios.objects.get(id=id)
    formulario = StaffForm(request.POST or None, request.FILES or None, instance=pendiente)
    
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect("staff-admin")


    return render(request,"administracion/staff/staff_editar.html", 
        {
            'sesion': inLogin, 
            'nombre':nombre, 
            'apellido':apellido, 
            'sexo':sexo, 
            'correo':correo, 
            'staff':nivel_staff,
            'formulario':formulario,
        })

def eliminar_staff(request, id):
    prod = Usuarios.objects.get(id=id)
    prod.delete()

    messages.warning(request, '¡Haz eliminado al Staff con ID: '+ str(id) +'!')
    return redirect('staff-admin')


######################################################################

def bandeja_admin(request):
    global inLogin
    global nombre
    global apellido
    global sexo
    global correo
    global nivel_staff


    buscador = request.GET.get("b_bandeja")
    promos = Bandeja.objects.all()

    if buscador:
        promos = Bandeja.objects.filter(email__icontains=buscador)


    return render(request,"administracion/bandeja/bandeja_admin.html", 
        {
            'sesion': inLogin, 
            'nombre':nombre, 
            'apellido':apellido, 
            'sexo':sexo, 
            'correo':correo, 
            'staff':nivel_staff,
            'pedidos': promos
        })

def editar_bandeja(request, id):
    global inLogin
    global nombre
    global apellido
    global sexo
    global correo
    global nivel_staff

    pendiente = Bandeja.objects.get(id=id)
    formulario = BandejaForm(request.POST or None, request.FILES or None, instance=pendiente)
    
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect("bandeja-admin")


    return render(request,"administracion/bandeja/bandeja_editar.html", 
        {
            'sesion': inLogin, 
            'nombre':nombre, 
            'apellido':apellido, 
            'sexo':sexo, 
            'correo':correo, 
            'staff':nivel_staff,
            'formulario':formulario,
        })

def eliminar_bandeja(request, id):
    prod = Bandeja.objects.get(id=id)
    prod.delete()

    messages.warning(request, '¡Haz eliminado la Bandeja con ID: '+ str(id) +'!')
    return redirect('bandeja-admin')

########################################################################################

############################# SISTEMA DE PROMOCIONES ###################################

########################################################################################

def agregar_promocion(request, id):
    global inLogin
    global nombre
    global apellido
    global sexo
    global correo
    global nivel_staff
    global cliente_unico

    promo = Promociones.objects.all()
    cliente = Clientes_Promocionados.objects.all()

    no_registrado = False
    for v in promo:
        if v.id == id: #1 en 1 de las promociones, es para verificar que el id de la promoción existe. Si no existe mandará un código de error
            for k in cliente: # 1 en 1 en la tabla de clientes promocionados....
                if k.cliente == cliente_unico:
                    no_registrado = True
                    messages.warning(request, '¡Usted ya canjeó un cupón :(!')
                    return redirect('promociones')
                        
            if not no_registrado:
                Clientes_Promocionados(
                    cliente=cliente_unico,
                    vencimiento=v.fecha_fin,
                    porcentaje_descuento=v.porcentaje_descuento,
                    promocion=id,
                    promocion_name=v.nombre,
                ).save()
                messages.warning(request, '¡¡Felicidades!! Tiene un nuevo cupón para utilizar')
                return redirect('promociones')


########################################################################################

############################# SISTEMA DE COMPRAS #######################################

########################################################################################

#carro = [ ['producto','cantidad','precio unitario','total'] ]

def carrito_compras(request, id):
    global suscrito

    agregado = False
    productos = Productos.objects.all()
    for v in productos:
        if v.id == id:
            if v.stock > 0:
                for k in carro:

                    if k['id'] == v.id:
                        agregado = True
                        messages.warning(request, '¡Ya añadiste este producto a tu carrito!')
                        return redirect('producto')

                if not agregado:
                    if suscrito:
                        precio_dsct = int(v.precio-((v.precio*5)/100))
                        carrito = {
                            'id': v.id,
                            'producto': v.producto,
                            'cantidad': 1,
                            'precio': precio_dsct,
                            'total': precio_dsct,
                            'categoria': 'producto',
                        }
                        carro.append(carrito)
                        messages.warning(request, '¡Ha sido añadido a tu carrito de compras!')
                        pedido=''

                        for k in carro:
                            pedido += k['producto']+' '
                        return redirect('producto')
                    else:
                        carrito = {
                            'id': v.id,
                            'producto': v.producto,
                            'cantidad': 1,
                            'precio': v.precio,
                            'total': v.precio,
                            'categoria': 'producto',
                        }
                        carro.append(carrito)
                        messages.warning(request, '¡Ha sido añadido a tu carrito de compras!')
                        pedido=''

                        for k in carro:
                            pedido += k['producto']+' '
                        return redirect('producto')
            else:
                messages.warning(request, '¡Producto Agotado!')


def servicio_carrito(request, id):
    agregado = False
    servicios = Servicios.objects.all()
    for v in servicios:
        if v.id == id:
            for k in carro:

                if k['id'] == v.id:
                    agregado = True
                    messages.warning(request, '¡Ya añadiste este producto a tu carrito!')
                    return redirect('servicio')

            if not agregado:
                carrito_p = {
                    'id': v.id,
                    'producto': v.producto,
                    'cantidad': 1,
                    'precio': v.precio,
                    'total': v.precio,
                    'categoria': 'servicio',
                }
                carro.append(carrito)
                messages.warning(request, '¡Ha sido añadido a tu carrito de compras!')
                pedido=''
                for k in carro:
                    pedido += k['producto']
                return redirect('servicio')

promo_activa = False   
nombre_promo = ''
desct_promo = 0

def activar_promocion(request):
    global inLogin
    global nombre
    global apellido
    global sexo
    global correo
    global cliente_unico

    global nombre_promo
    global desct_promo
    global promo_activa

    if inLogin:
        try:
            promocionado = Clientes_Promocionados.objects.get(cliente=cliente_unico)
            desct_promo = promocionado.porcentaje_descuento
            nombre_promo = promocionado.promocion_name
            promo_activa = True
        except:
            messages.warning(request, '¡No tienes cupones para canjear!')
    else:
        messages.warning(request, '¡Sin sesión Iniciada!')

    return redirect('carrito')

def carrito(request):
    global inLogin
    global nombre
    global apellido
    global sexo
    global correo
    global cliente_unico

    global carro
    global calle_envio
    global comuna_envio
    global ciudad_envio

    global nombre_promo
    global desct_promo
    global promo_activa

    total = 0

    productos = Productos.objects.all()

    calle = request.GET.get("calle")
    comuna = request.GET.get("comuna")
    ciudad = request.GET.get("ciudad")

    if inLogin:
        try:
            promocionados = Clientes_Promocionados.objects.get(cliente=cliente_unico)
        except:
            promocionados = {
                'cliente': '-',
                'vencimiento': '0/00/0000',
                'porcentaje_descuento': 0,
                'promocion': 0,
                'promocion_name': 'Sin Cupón',
            }

    for v in productos:
        for k in carro:
            if k['id'] == v.id:
                total += k['total']


    if promo_activa:
        dsc = (total*desct_promo)//100
        total -= dsc


    if calle or comuna or ciudad:

        calle_envio  = calle
        comuna_envio = comuna
        ciudad_envio = ciudad
        messages.warning(request, '¡Actualizaste tu zona de envío correctamente!')
        return render(request,"carrito.html", 
                {
                    'sesion': inLogin, 
                    'nombre':nombre, 
                    'apellido':apellido, 
                    'sexo':sexo, 
                    'correo':correo, 
                    'carro':carro,
                    'pagar':total,
                    'calle_envio':calle_envio,
                    'comuna_envio':comuna_envio,
                    'ciudad_envio':ciudad_envio,
                    'disponible': True,
                    'zona_pago': True,
                    'promocionados':promocionados,
                    'unico_cliente':cliente_unico,
                })

    if len(carro) > 0:
        if calle_envio == '' or comuna_envio == '' or ciudad_envio == '':
            return render(request,"carrito.html", 
                {
                    'sesion': inLogin, 
                    'nombre':nombre, 
                    'apellido':apellido, 
                    'sexo':sexo, 
                    'correo':correo, 
                    'carro':carro,
                    'pagar':total,
                    'calle_envio':calle_envio,
                    'comuna_envio':comuna_envio,
                    'ciudad_envio':ciudad_envio,
                    'disponible': True,
                    'zona_pago': False,
                })
        else:
            return render(request,"carrito.html", 
                {
                    'sesion': inLogin, 
                    'nombre':nombre, 
                    'apellido':apellido, 
                    'sexo':sexo, 
                    'correo':correo, 
                    'carro':carro,
                    'pagar':total,
                    'calle_envio':calle_envio,
                    'comuna_envio':comuna_envio,
                    'ciudad_envio':ciudad_envio,
                    'disponible': True,
                    'zona_pago': True,
                    'promocionados':promocionados,
                    'unico_cliente':cliente_unico,
                })
    else:
        return render(request,"carrito.html", 
        {
            'sesion': inLogin, 
            'nombre':nombre, 
            'apellido':apellido, 
            'sexo':sexo, 
            'correo':correo, 
            'carro':carro,
            'pagar':total,
            'disponible': False,
            

        })

def aumentar_carrito(request, producto):
    global carro
    productos = Productos.objects.all()
    
    for k in carro:
        if k['producto'] == producto:
                        
            for v in productos:
                if v.stock > k['cantidad']:
                    k['cantidad'] += 1
                    k['total'] =  k['cantidad'] * k['precio']
                    return redirect('carrito')
                else:
                    messages.warning(request, '¡Supera el límite de stock!')
                    return redirect('carrito')

def descontar_carrito(request, producto):
    global carro

    for k in carro:
        if k['producto'] == producto:
            if k['cantidad'] <= 1:
                carro.remove(k)
            else:
                k['cantidad'] -= 1
                k['total'] =  k['cantidad'] * k['precio']
            return redirect('carrito')

def borrar_carrito(request, producto):
    global carro

    for k in carro:
        if k['producto'] == producto:
            carro.remove(k)
            return redirect('carrito')


def pagar(request):
    global inLogin
    global nombre
    global apellido
    global sexo
    global correo
    global carro
    global calle_envio
    global comuna_envio
    global ciudad_envio
    global cliente_unico
    global nombre_promo
    global desct_promo
    global promo_activa

    total = 0
    pedido = ''
    productos = Productos.objects.all()

    for k in carro:
        pedido += 'x'+str(k['cantidad'])+' '+k['producto']+' - '
        for v in productos:
            if k['id'] == v.id:
                total += k['total']
                v.stock -= k['cantidad']
                v.save()

    clientes = Clientes.objects.all()

    if promo_activa:
        dsc = (total*desct_promo)//100
        total -= dsc
        promo_activa = False
        desct_promo = 0
        promo_activa = False
        promo = Clientes_Promocionados.objects.get(cliente=cliente_unico)
        promo.delete()

    for user in clientes:
        if user.email == correo and user.nombre == nombre and user.apellido == apellido and user.sexo == sexo:
            Pedidos(
                cliente= user.nombre_unico,
                producto= pedido,
                fecha_pedido= date.today().strftime('%Y-%m-%d'),
                fecha_entrega= date.today().strftime('%Y-%m-%d'),
                total= total,
                prioridad= 0,
                numero_seguimiento = '0',
                estado = 'Preparando',
                calle_envio= calle_envio,
                comuna_envio= comuna_envio,
                ciudad_envio = ciudad_envio,
            ).save()

            carro = []
            messages.warning(request, '¡Compra realizada con éxito!')

    return render(request,"carrito.html", 
        {
            'sesion': inLogin, 
            'nombre':nombre, 
            'apellido':apellido, 
            'sexo':sexo, 
            'correo':correo, 
            'carro':carro,
            'pagar':total,
        })





def suscribirme(request):
    global inLogin
    global nombre
    global apellido
    global sexo
    global correo

    cliente = Clientes.objects.filter(email=correo)
    if request.method == 'POST': 
        for v in cliente:
            if v.suscrito:
                messages.warning(request, '¡Tu ya estás suscrito!')
                return redirect("suscripcion")
            else:
                v.suscrito = True
                v.save()
                messages.warning(request, '¡Te has suscrito con éxito!')
                return redirect("suscripcion")

    return render(request,"promociones/suscribirme.html", 
        {
            'sesion': inLogin, 
            'nombre':nombre, 
            'apellido':apellido, 
            'sexo':sexo, 
            'correo':correo,
        })