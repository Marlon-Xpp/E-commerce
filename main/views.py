from django.shortcuts import render, redirect
from main.models import Company
import random
from django.core.mail import send_mail
from ecommers import settings
from django.contrib.auth import logout
from products.models import Product, Cart, CartItem
# from products.views import get_products_id
# Create your views here.

def get_company_data():
    
    company = Company.objects.first()
    exist = Company.objects.exists()
    count = Company.objects.count()
    
    if exist:
        print(f"Hay solo {count} tabla en Compania")
        return company  # Obtén el primer objeto de Company
        
    else:
        return "No hay registro"       



def get_email_password():
    
    email = Company.objects.values_list('email', flat=True).first()
    # password = Company.objects.values_list('passsword', flat=True).first()
    
    if len(email) != 0:
        print(f"Si existe el email: {email}")
        return email
    else:
        return "No existe email"


def home(request):
    company_data = get_company_data()  # Llama a la función para obtener los datos
    products = list(Product.objects.all())
    
    if len(products) != 0:
        print(f"Si hay prodcutos: {products}")
    else:
        print("no hay prodcutos")
        
    #obtener productos aleatorios
    random_products = random.sample(products, min(len(products), 5))
    #obtener los 3 ultimos productos
    latest_products = Product.objects.order_by("-date_added")[:3]
    #obtener los 3 primeros productos
    first_products = Product.objects.order_by("date_added")[:3]
    # Obtener los 3 productos con más likes (mejores valorados)
    top_rated_products = Product.objects.order_by("-likes")[:3]


    if request.user.is_authenticated:
        # Si el usuario está autenticado, obtenemos o creamos el carrito
        cart, created = Cart.objects.get_or_create(user=request.user)
        # Contar el número total de productos en el carrito
        total_items = sum(item.quantity for item in cart.items.all())
    else:
        # Si el usuario no está autenticado, no se crea un carrito, solo asignamos 0 productos
        cart = None  # No hay carrito para usuarios no autenticados
        total_items = 0  # Por defecto, el total de productos es 0

    
    return render(request, "index.html", 
                {"random_products": random_products,
                "company_data": company_data,
                "latest_products": latest_products,
                "first_products": first_products,
                "top_rated_products": top_rated_products,
                # "product": get_products_id(product_id)
                "cart": cart,
                "total_items":total_items,
                })




def blog_details(request):
    company_data = get_company_data()  # Llama a la función para obtener los datos
    return render(request, "blog-details.html", {"company_data": company_data})

def blog(request):
    company_data = get_company_data()  # Llama a la función para obtener los datos
    return render(request, "blog.html", {"company_data": company_data})




def contact(request):
    company_data = get_company_data()  # Llama a la función para obtener los datos
    print(f"el resultado: {company_data}")
    
    # email = get_email_password()
    # print(f"obtener email: {email}")
    
    
    if request.user.is_authenticated:
        # Si el usuario está autenticado, obtenemos o creamos el carrito
        cart, created = Cart.objects.get_or_create(user=request.user)
        # Contar el número total de productos en el carrito
        total_items = sum(item.quantity for item in cart.items.all())
    else:
        # Si el usuario no está autenticado, no se crea un carrito, solo asignamos 0 productos
        cart = None  # No hay carrito para usuarios no autenticados
        total_items = 0  # Por defecto, el total de productos es 0

    
    if request.method == "POST":
        
        
        name_client = request.POST.get("name").strip()
        email_client = request.POST.get("email").strip()
        message = request.POST.get("message").strip()
        
        print(f"""
                Nombre = {name_client}
                Correo = {email_client}
                Mensaje = {message}
                """)
    
        send_email(name_client, email_client, message)
        
    return render(request, "contact.html", 
            {
            "company_data": company_data,
            "cart": cart,
            "total_items":total_items,
            })



def send_email(name_client, email_client, message):
    try:
        company = Company.objects
        #obtener el email de la empresa
        email = company.values_list("email", flat=True).first()
        #obtener el password de la empresa
        password = company.values_list("password", flat=True).first()

        # Configuración del correo
        
        email_host_user = email
        email_host_password = password
        
        
        # Configuración del correo
        # EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
        # EMAIL_HOST = 'smtp.gmail.com'
        # EMAIL_PORT = 587
        # EMAIL_USE_TLS = True
        
        print(f"email host user: {email_host_user}")
        print(f"email host password: {email_host_password}")
        
        
        if email and password:
            print(f"El correo y la contraseña si existe")
            
            send_mail(
                "Mensaje Del Cliente",#asunto
                f"Nombre Del Cliente: {name_client}\nMensaje: {message}\nCorreo Del Cliente: {email_client}", #mensaje
                email_client, #remitente
                [settings.EMAIL_HOST_USER], #email destinatario
                fail_silently=False #detectar algun error
            )
            
            print(f"Se envio Correctamente con exito al correo: {name_client}")
            # return redirect ("contact")
            return (f"Se envio Correctamente con exito al correo: {name_client}")
        else:
            print(f"El correo NO existe")
            return "El correo NO existe"
        
    except Exception as e:
        print(f"Hubo un error: {e}")
        return "Hubo un error al enviar el correo"
    
    
    

#Funcion para buscar productos creando un ruta exclusivamente para esta funcion con 
#Gracias al form action le pasamos la ruta cuadno se ejecuta el form
def search_products(request):
    company_data = get_company_data()  # Llama a la función para obtener los datos
    has_products = Product.objects.all().exists()  # Verifica si hay productos 
    products_with_discounts =Product.objects.filter(discount__gt=0)
    has_promotions = products_with_discounts.exists()
    query = request.GET.get("search", "").lower()  # Captura el término de búsqueda desde el parámetro GET
    
    #obtener productos mas vendidos
    more_sale = Product.objects.order_by("-sales")[:3]
    #obtener categorias
    get_category = Product.objects.values_list('category', flat=True).distinct()
    
    if request.user.is_authenticated:
        # Si el usuario está autenticado, obtenemos o creamos el carrito
        cart, created = Cart.objects.get_or_create(user=request.user)
        # Contar el número total de productos en el carrito
        total_items = sum(item.quantity for item in cart.items.all())
    else:
        # Si el usuario no está autenticado, no se crea un carrito, solo asignamos 0 productos
        cart = None  # No hay carrito para usuarios no autenticados
        total_items = 0  # Por defecto, el total de productos es 0

    
    
    print(f"buscaste: {query}")
    
    if query:
        products = Product.objects.filter(name__icontains=query) #busqueda parcial palabra x plabras en ves de la plabra exacta
    else:
        Product.objects.all()  # Si no hay búsqueda, muestra todos los productos
    
    return render(request, 'shop-grid.html', {
        'products': products, 
        'search_query': query, 
        "has_products": has_products,
        "has_promotions" : has_promotions,
        "products_with_discounts" : products_with_discounts,
        "company_data": company_data,
        "more_sale": more_sale,
        "get_category": get_category,
        
        "cart": cart,
        "total_items":total_items,
        })


    
    
def exit(request):
    logout(request)
    print("capturando la funcion")
    return redirect("home")