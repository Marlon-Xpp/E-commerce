# Generated by Django 5.1.1 on 2024-11-19 20:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CartItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.PositiveIntegerField(default=1)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Cart",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("items", models.ManyToManyField(blank=True, to="products.cartitem")),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=255, verbose_name="Nombre del Producto"
                    ),
                ),
                (
                    "description",
                    models.TextField(verbose_name="Descripción del Producto"),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        verbose_name="Precio del Producto",
                    ),
                ),
                (
                    "brand",
                    models.CharField(max_length=255, verbose_name="Marca del Producto"),
                ),
                (
                    "stock",
                    models.PositiveIntegerField(verbose_name="Stock del Producto"),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to="products/", verbose_name="Imagen del Producto"
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("bebida", "Bebidas"),
                            ("lacteos_panaderia", "Lacteos y Panaderia"),
                            ("conservas_enlatados", "Conservas y Enlatados"),
                            ("productos_limpieza", "Productos de Limpieza"),
                            ("productos_extras", "Productos Extras"),
                        ],
                        max_length=255,
                        verbose_name="Categoría del Producto",
                    ),
                ),
                (
                    "featured",
                    models.BooleanField(
                        default=False, verbose_name="Producto Destacado"
                    ),
                ),
                (
                    "date_added",
                    models.DateTimeField(auto_now_add=True, verbose_name="Fecha"),
                ),
                (
                    "likes",
                    models.PositiveIntegerField(
                        default=0, verbose_name="Me gustas del Producto"
                    ),
                ),
                (
                    "sales",
                    models.PositiveIntegerField(
                        default=0, verbose_name="Cantidad Vendida del Producto"
                    ),
                ),
                (
                    "weight",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=20,
                        verbose_name="Peso del Producto",
                    ),
                ),
                (
                    "unit_weight",
                    models.CharField(
                        choices=[
                            ("kg", "Kilogramo"),
                            ("g", "Gramo"),
                            ("mg", "Miligramo"),
                            ("lb", "Libra"),
                            ("oz", "Onza"),
                        ],
                        max_length=2,
                        verbose_name="Unidad de peso",
                    ),
                ),
                (
                    "discount",
                    models.PositiveIntegerField(
                        blank=True,
                        choices=[
                            (5, "5%"),
                            (10, "10%"),
                            (15, "15%"),
                            (20, "20%"),
                            (30, "30%"),
                        ],
                        default=0,
                        null=True,
                        verbose_name="Descuento del Producto",
                    ),
                ),
                (
                    "liked_by",
                    models.ManyToManyField(
                        blank=True,
                        related_name="liked_products",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="cartitem",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="products.product"
            ),
        ),
    ]
