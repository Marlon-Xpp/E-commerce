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

# Create your views here.
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



def method_buy(request):

    fact_user = []
    if  request.method == "POST":
        name = request.POST.get('name')  # Retrieves 'example_value'
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        direction = request.POST.get('direction')
        
        fact_user.append(name,lastname,username,phone,direction)


    # Configura MercadoPago
    mp = mercadopago.SDK(settings.MERCADOPAGO_TEST_ACCESS_TOKEN)
    mp.advanced_payment()
    
    
    #capturando la funcion session
    cart_details = request.session.get('cart_details', {
        'cart': None,
        'total_items': None,
        'price_total': None,
    })

    # Generar URLs dinámicamente
    pending_url = request.build_absolute_uri(reverse('pending'))
    success_url = request.build_absolute_uri(reverse('success'))
    failure_url = request.build_absolute_uri(reverse('failure'))
    
    
    # Crear la lista de items
    items = []
    for cart in cart_details['items']:
        item = {
            "title": cart['product_name'],              # Nombre del producto
            "description": cart['product_name'],   # Descripción
            "quantity": cart['quantity'],                         # Cantidad
            "unit_price": float(cart['price']),  # Precio
        }
        items.append(item)
    
    
        # Definir el payer (comprador)
    
    
    
    
    payer = {
    "name": "Juan Pérez",            # Nombre del comprador
    "surname": "González",           # Apellido del comprador
    "email": "juan.perez@example.com", # Correo electrónico
    "identification": {
        "type": "DNI",               # Tipo de identificación (DNI, Pasaporte, etc.)
        "number": "12345678"         # Número de identificación
    },
    "phone": {
        "area_code": "11",           # Código de área
        "number": "123456789"        # Número de teléfono
    }
}
    
    # Crear la preferencia con categoría
    preference_data = {
        "items":    items,
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
        # return JsonResponse({"payment_link": preference_response["response"]["init_point"]})
        return redirect(preference_response["response"]["sandbox_init_point"])
    else:
        return JsonResponse({"error": "No se pudo crear la preferencia de pago"}, status=400)
    























def success_page(request):
# Captura el payment_id de la query string
    payment_id = request.GET.get('payment_id')

    if payment_id:
   # Inicializa la SDK de MercadoPago con tu access token
        mp = mercadopago.SDK(settings.MERCADOPAGO_TEST_ACCESS_TOKEN)

        # Obtener los detalles del pago usando el payment_id
        payment = mp.payment().get(payment_id)

    if payment['status'] == 200:
        # Obtener la información del pago
        payment_details = payment['response']
       
        enviar_correo_simple(
        destinatario="gespinozaprudencio@gmail.com",
        asunto="Tu factura de compra",
        mensaje=render_to_string(
        'verify/success.html',  # Ruta de la plantilla
        {
            'payment_details': payment_details,
            
        }))
    
        
        return render(request, "verify/success.html", {"payment_details": payment_details})

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
    send_mail(
        asunto,  # Asunto del correo
        mensaje,  # Mensaje
        'gespinoza1@autonoma.edu.pe',  # Remitente
        [destinatario],  # Destinatarios
        fail_silently=False,  # No ignorar errores
        html_message=mensaje  # Mensaje en formato HTML
    )
    print("correo")