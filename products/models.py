from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

class Product(models.Model):
    
    UNIT_WEIGHT = [
        ('kg', 'Kilogramo'),
        ('g', 'Gramo'),
        ('mg', 'Miligramo'),
        ('lb', 'Libra'),
        ('oz', 'Onza'),
    ]
    
    OPTION_DISCOUNT =  [
        (5, '5%'),
        (10, '10%'),
        (15, '15%'),
        (20, '20%'),
        (30, '30%'),
    ]
    
    OPTION_CATEGORY =  [
        ('Leche', 'Leche'),
        ('Aceites', 'Aceites'),
        ('Chocolates', 'Chocolates'),
        ('Frijoles', 'Frijoles'),
        ('Higiene_Dental', 'Higiene Dental'),
        ('Fórmulas Infantiles', 'Fórmulas Infantiles'),
        ('Dulces', 'Dulces'),
        ('Galleta', 'Galleta'),
        ('Productos Extras', 'Productos Extras'),
        
    ]
    
    name = models.CharField(max_length=255, verbose_name="Nombre del Producto")  # Nombre del producto
    description = models.TextField(verbose_name="Descripción del Producto")  # Descripción detallada del producto
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio del Producto")  # Precio del producto
    brand = models.CharField(max_length=255, verbose_name="Marca del Producto")  # Marca o fabricante del producto
    stock = models.PositiveIntegerField(verbose_name="Stock del Producto")  # Cantidad de stock disponible
    image = models.ImageField(upload_to='products/', verbose_name="Imagen del Producto")  # Imagen del producto
    category = models.CharField(choices=OPTION_CATEGORY, max_length=255, verbose_name="Categoría del Producto")  # Categoría del producto (ej: "Frutas", "Verduras")
    featured = models.BooleanField(default=False, verbose_name="Producto Destacado")  # Indica si el producto es destacado o no
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Fecha")  # Fecha en que se añadió el producto
    likes = models.PositiveIntegerField(default=0, verbose_name="Me gustas del Producto")  # Número de "me gusta" o valoraciones del producto
    sales = models.PositiveIntegerField(default=0, verbose_name="Cantidad Vendida del Producto")  # Cantidad de veces que se ha vendido el producto
    weight = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Peso del Producto")
    unit_weight = models.CharField(max_length=2, verbose_name="Unidad de peso", choices=UNIT_WEIGHT)  
    discount = models.PositiveIntegerField(choices=OPTION_DISCOUNT, default=0, null=True, blank=True, verbose_name="Descuento del Producto")  # Limitar las opciones de descuento # Cambié max_length y agregué un valor por defecto
    
    
    liked_by = models.ManyToManyField(User, related_name='liked_products', blank=True)  # Identificar a los usuarios que le dieron like
    
    
    # Funcion parar calcular el descuento
    def price_discount(self):
        """Calcula el precio aplicando el descuento si es mayor a 0."""
        if self.discount > 0:
            discount_decimal = Decimal(self.discount) / Decimal(100)
            result = self.price * (1 - discount_decimal)
            return round(result, 2)
        return round(self.price, 2)
    
    def __str__(self):
        return self.name



class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    
    def total_price(self):
        """Calcula el precio total usando el precio con descuento si existe."""
        """Calcula el precio total usando el precio con descuento si existe."""
        if self.product.discount is not None and self.product.discount > 0:  # Verifica si discount no es None y es mayor a 0
            discounted_price = self.product.price_discount()  # Precio con descuento
            return discounted_price * self.quantity
        else:  # Sin descuento o si discount es None
            return self.product.price * self.quantity
        
        # """Calcula el precio total considerando el descuento si existe."""
        # discounted_price = self.product.price_discount()  # Calcula el precio con descuento
        # return discounted_price * self.quantity

    def __str__(self):
        return( 
                f"{self.quantity} of {self.product.name} - "
                f"Discounted Price: {self.product.price_discount()} each, "
                f"Total: {self.total_price()}"
                )

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem, blank=True)

    def subtotal(self):
        return sum(item.total_price() for item in self.items.all())

    def __str__(self):
        return f"Cart for {self.user.username}"
