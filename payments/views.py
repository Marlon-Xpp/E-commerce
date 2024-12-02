from django.shortcuts import render , redirect
import mercadopago
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import JsonResponse 
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from main.views import get_company_data
from products.models import Product, Cart, CartItem
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def checkout(request):
    
    
    if request.user.is_authenticated:
        # Si el usuario está autenticado, obtenemos o creamos el carrito
        cart, created = Cart.objects.get_or_create(user=request.user)
        # Contar el número total de productos en el carrito
        total_items = sum(item.quantity for item in cart.items.all())
        
    else:
        # Si el usuario no está autenticado, no se crea un carrito, solo asignamos 0 productos
        cart = None  # No hay carrito para usuarios no autenticados
        total_items = 0  # Por defecto, el total de productos es 0
        
    # Contar el número de productos que el usuario ha marcado como favoritos
    favorite_products_count = Product.objects.filter(liked_by=request.user).count() if request.user.is_authenticated else 0  
    print(f"obtuvo esto: {favorite_products_count}")
    
    #request.session.flush()
    return render(request, "checkout.html",{
        "cart": cart,
        "total_items":total_items,
        "company_data": get_company_data(),
        "favorite_products_count":favorite_products_count,
    })


@login_required
def method_buy(request):
    
    print("Entrando a la funcion POST")
    if  request.method == "POST":
        
        firstname = request.POST.get('firstname')  # Retrieves 'example_value'
        lastname = request.POST.get('lastname')
        # username = request.POST.get('username')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        email = request.POST.get("email")
        
        
        
        print(f"Añadiendo los campos en una session temporal")
        # request.session['firstname'] = firstname
        # request.session['lastname'] = lastname 
        # request.session['phone'] = phone 
        request.session['address'] = address  
        request.session['email'] = email 
        print("Se añadio exitosamente")
        
        print(f"""
                nombre = {firstname}
                apellidos = {lastname}
                telefono = {phone}
                direccion = {address}
                correo = {email}
            """)
        
        
        
    # Configura MercadoPago
    mp = mercadopago.SDK(settings.MERCADOPAGO_TEST_ACCESS_TOKEN)
    mp.advanced_payment()
    
    
    # #capturando la funcion session lo cual debe eliminarse
    # cart_details = request.session.get('cart_details', {
    #     'cart': None,
    #     'total_items': None,
    #     'price_total': None,
    # })
    
    
    if request.user.is_authenticated:
        # Si el usuario está autenticado, obtenemos o creamos el carrito
        cart, created = Cart.objects.get_or_create(user=request.user)
        # Contar el número total de productos en el carrito
        # total_items = sum(item.quantity for item in cart.items.all())
    else:
        # Si el usuario no está autenticado, no se crea un carrito, solo asignamos 0 productos
        cart = None  # No hay carrito para usuarios no autenticados
        # total_items = 0  # Por defecto, el total de productos es 0
        
    # Generar URLs dinámicamente
    pending_url = request.build_absolute_uri(reverse('pending'))
    success_url = request.build_absolute_uri(reverse('success'))
    failure_url = request.build_absolute_uri(reverse('failure'))
    
    # Crear la lista de items
    items = []
    
    for cart in cart.items.all():
        
        # Verifica si hay descuento y maneja el caso en que sea None
        if cart.product.discount is not None and cart.product.discount > 0:
            unit_price = float(cart.product.price_discount())  # Precio con descuento
        else:
            unit_price = float(cart.product.price)  # Precio original
        
        item = {
            "title": cart.product.name,  # Nombre del producto
            "description": cart.product.name, # Descripción
            "quantity": cart.quantity,  # Cantidad
            
            "unit_price": unit_price, # Precio
        }
        
        items.append(item)
    
    
    
    
    
    # Definir el payer (comprador)
    payer = {
        "name": firstname,            # Nombre del comprador
        "surname": lastname,           # Apellido del comprador
        "email": email, # Correo electrónico
        "identification": {
            "type": "DNI",               # Tipo de identificación (DNI, Pasaporte, etc.)
            "number": "12345678"         # Número de identificación
        },
        "phone": {
            "area_code": "51",           # Código de área
            "number": phone,        # Número de teléfono
        }
    }
    
    # Crear la preferencia con categoría
    preference_data = {
        "items": items,
        "payer": payer,
        
        "back_urls": {
            "success": success_url,
            "failure": failure_url,
            "pending": pending_url,

        },
        "auto_return": "approved",
        "sandbox_init_point": True,
    }

    # Crear la preferencia en MercadoPago
    preference_response = mp.preference().create(preference_data)

    if preference_response['status'] == 201:
        # URL del checkout  
        print("EXITO en la respuesta del servidos")
        # return JsonResponse({"payment_link": preference_response["response"]["init_point"]})
        return redirect(preference_response["response"]["sandbox_init_point"])
    else:
        return JsonResponse({"error": "No se pudo crear la preferencia de pago"}, status=400)
    

@login_required
def success_page(request):
# Captura el payment_id de la query string
    payment_id = request.GET.get('payment_id')

    if payment_id:
    # Inicializa la SDK de MercadoPago con tu access token
        mp = mercadopago.SDK(settings.MERCADOPAGO_TEST_ACCESS_TOKEN)

        # Obtener los detalles del pago usando el payment_id
        payment = mp.payment().get(payment_id)
        print(payment_id)
        
    if payment['status'] == 200:
        # Obtener la información del pago
        payment_details = payment['response']
        
        #print(payment['response']['additional_info'])
        #Capturamos el email del cliente desde la session temporalmente
        email = request.session.get("email","Correo No Disponible")
        address = request.session.get("address","Direccion No Disponible")
        
        if request.user.is_authenticated:
            # Si el usuario está autenticado, obtenemos o creamos el carrito
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            # Si el usuario no está autenticado, no se crea un carrito, solo asignamos 0 productos
            cart = None  

        
        enviar_correo_simple(
        #correo del cliente estatico, OBSERVACION CAMBIO
        destinatario=email,
        #Asunto del mensaje del correo
        asunto="Tu factura de compra",
        
        mensaje=render_to_string(
        'verify/success.html',  # Ruta de la plantilla
        {
            'payment_details': payment_details,
            'email': email,
            "address": address,
        }))
        return render(request, "verify/success.html", {
            "payment_details": payment_details,
            'email': email,
            "cart":cart,
            "address":address,
            })

    else:
        return JsonResponse({"error": "No se proporcionó el payment_id"}, status=400)


def failure_page(request):
    
    return render(request,"verify/failure.html",{})

def pending_page(request):
    
    return render(request,"verify/pending.html",{})


def get_payment_details(request, payment_id):
    # Inicializa la SDK de MercadoPago con tu access token
    mp = mercadopago.SDK(settings.MERCADOPAGO_TEST_ACCESS_TOKEN)



    # Obtener los detalles del pago usando el payment_id
    payment = mp.payment().get(payment_id)

    if payment['status'] == 200:
        # Obtener la información del pago
        payment_details = payment['response']
        payer = payment_details['payer']  # Información del comprador
        
        # Verificar si existen items en el pago
        items = payment_details['additional_info']['items']  # Si no existe 'items', se asigna una lista vacía
        transaction_amount = payment_details['transaction_amount']  # Monto total
        date_approved = payment_details['date_approved']  # Fecha de aprobación

        # Aquí puedes crear la factura con estos datos
        return JsonResponse({
            'payer': payer,
            'items': items,
            'transaction_amount': transaction_amount,
            'date_approved': date_approved,
        })
    else:
        return JsonResponse({"error": "No se pudo obtener el pago."}, status=400)
    
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart




def enviar_correo_simple(destinatario, asunto, mensaje):

    #correo de la empresa
    email = settings.DEFAULT_FROM_EMAIL
    
    send_mail(
        asunto,  # Asunto del correo
        mensaje,  # Mensaje
        email,  # Remitente dinamico, CORREO DE LA EMPRESA 
        [destinatario],  # Destinatarios
        fail_silently=False,  # No ignorar errores
        html_message=mensaje  # Mensaje en formato HTML
    )
    print(f"El mensaje se envio al correo del cliente {email}")