from django.urls import path
from products import views


urlpatterns = [
    
    path("shop-details/<int:product_id>/", views.shop_details , name="shop-details"),
    # path("shoping-cart/<int:product_id>/", views.shoping_cart , name="shoping-cart"),
    path("shop-grid/", views.shop_grid , name="shop-grid"),
    
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart-item/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/', views.cart_detail, name='cart_detail'),
    
    path('category/<str:category>/', views.products_by_category, name='products_by_category'),
] 