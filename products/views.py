from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from products.models import Product
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from main.views import get_company_data
from django.http import JsonResponse
from .models import Product, Cart, CartItem

# Create your views here.


def get_products_id(product_id):
    product = get_object_or_404(Product, id=product_id)
    return product

def shop_details(request, product_id):
    # add_favorite()
    # if request.method == "POST":
    #     quantity = request.POST.get("quantity", 1)
    #     print(f"cantidad: {quantity}")
        
    if request.user.is_authenticated:
        # Si el usuario está autenticado, obtenemos o creamos el carrito
        cart, created = Cart.objects.get_or_create(user=request.user)
        # Contar el número total de productos en el carrito
        total_items = sum(item.quantity for item in cart.items.all())
    else:
        # Si el usuario no está autenticado, no se crea un carrito, solo asignamos 0 productos
        cart = None  # No hay carrito para usuarios no autenticados
        total_items = 0  # Por defecto, el total de productos es 0

    
    return render(request, "shop-details.html", {
        "product": get_products_id(product_id),
        "company_data": get_company_data(),
        "cart": cart,
        "total_items":total_items,
    })

def shoping_cart(request, product_id):
    
    # # Paso 1: Obtener el producto por ID
    # products = get_object_or_404(Product, id=product_id)
    
    # # Paso 2: Capturar la información del producto
    # product_name = products.name
    # product_img = products.image
    # product_price = products.price
    
    # # Debug: mostrar la información del producto y el carrito
    # print(f"Producto añadido: {product_name}, {product_img}, {product_price}")
    
    return render(request, "shoping-cart.html",{
        # "products": products,  # Pasar todos los productos en el carrito
        "company_data": get_company_data(),
    })




def shop_grid(request):
    product_list = Product.objects.all()  # Obtiene todos los productos
    products_with_discounts = Product.objects.filter(discount__gt=0) # Filtrar los productos con descuentos activos (mayor a 0)
    total_products = product_list.count() #obtener total de productos
    
    paginator = Paginator(product_list, 12)  # 12 productos por página
    page_number = request.GET.get("page")  # Obtiene el número de página de la URL
    products = paginator.get_page(page_number)  # Obtiene los productos para la página actual
    
    has_products = product_list.exists()  # Verifica si hay productos 
    has_promotions =  products_with_discounts.exists() # verifica si Existen promociones
    
    #obtener los 3 ultimos productos
    latest_products = Product.objects.order_by("-date_added")[:3]
    #obtener categorias
    get_category = Product.objects.values_list('category', flat=True).distinct()
    
    #obtener productos mas vendidos
    more_sale = Product.objects.order_by("-sales")[:3]
    
    
    if request.user.is_authenticated:
        # Si el usuario está autenticado, obtenemos o creamos el carrito
        cart, created = Cart.objects.get_or_create(user=request.user)
        # Contar el número total de productos en el carrito
        total_items = sum(item.quantity for item in cart.items.all())
    else:
        # Si el usuario no está autenticado, no se crea un carrito, solo asignamos 0 productos
        cart = None  # No hay carrito para usuarios no autenticados
        total_items = 0  # Por defecto, el total de productos es 0

    
    return render(request, "shop-grid.html", {
        "products": products,
        "total_products": total_products,
        "has_products": has_products,
        "has_promotions":has_promotions,
        "products_with_discounts" : products_with_discounts,
        "company_data": get_company_data(),
        "latest_products": latest_products,
        "more_sale": more_sale,
        "get_category":get_category,
        "cart": cart,
        "total_items":total_items,
    })



def products_by_category(request, category):
    
    product_list = Product.objects.all()  # Obtiene todos los productos
    products_with_discounts = Product.objects.filter(discount__gt=0) # Filtrar los productos con descuentos activos (mayor a 0)
    total_products = product_list.count() #obtener total de productos
    
    paginator = Paginator(product_list, 12)  # 12 productos por página
    page_number = request.GET.get("page")  # Obtiene el número de página de la URL
    products = paginator.get_page(page_number)  # Obtiene los productos para la página actual
    
    has_products = product_list.exists()  # Verifica si hay productos 
    has_promotions =  products_with_discounts.exists() # verifica si Existen promociones
    
    #obtener los 3 ultimos productos
    latest_products = Product.objects.order_by("-date_added")[:3]
    #obtener categorias
    get_category = Product.objects.values_list('category', flat=True).distinct()
    #obtener productos mas vendidos
    more_sale = Product.objects.order_by("-sales")[:3]
    # Filtrar productos por categoría
    products = Product.objects.filter(category=category)
    
    
    if request.user.is_authenticated:
        # Si el usuario está autenticado, obtenemos o creamos el carrito
        cart, created = Cart.objects.get_or_create(user=request.user)
        # Contar el número total de productos en el carrito
        total_items = sum(item.quantity for item in cart.items.all())
    else:
        # Si el usuario no está autenticado, no se crea un carrito, solo asignamos 0 productos
        cart = None  # No hay carrito para usuarios no autenticados
        total_items = 0  # Por defecto, el total de productos es 0

    
    # Pasar los productos y el estado al contexto
    return render(request, 'shop-grid.html', {
        
        "products": products,
        "total_products": total_products,
        "has_products": has_products,
        "has_promotions":has_promotions,
        "products_with_discounts" : products_with_discounts,
        "company_data": get_company_data(),
        "latest_products": latest_products,
        "more_sale": more_sale,
        "get_category":get_category,
        "selected_category": category,
        "cart": cart,
        "total_items":total_items,
    })
    

# FUNCIONES DE CARRITO DE COMPRA
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    cart.items.add(cart_item)
    cart.save()

    return redirect('cart_detail')

@login_required
def remove_from_cart(request, item_id):
    cart = Cart.objects.get(user=request.user)
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart.items.remove(cart_item)
    cart_item.delete()

    return redirect('cart_detail')

@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if 'quantity' in request.POST:
        cart_item.quantity = int(request.POST['quantity'])
        cart_item.save()

    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Contar el número total de productos en el carrito
    total_items = sum(item.quantity for item in cart.items.all())
    
    return render(request, 'shoping-cart.html', 
                {'cart': cart, 
                "company_data": get_company_data(),
                'total_items': total_items
                })