from django.urls import path
from main import views


urlpatterns = [
    path("", views.home , name="home"),
    path("blog-details/", views.blog_details , name="blog-details"),
    # path("blog/", views.blog , name="blog"),
    path("contact/", views.contact , name="contact"),
    path("search_products/", views.search_products , name="search_products"),
    path('toggle-like/<int:product_id>/', views.toggle_like, name='toggle_like'),
    path("exit/", views.exit, name="exit"),
    
]
