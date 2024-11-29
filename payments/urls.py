from django.urls import path
from payments import views

urlpatterns = [
    path("checkout/", views.checkout , name="checkout"),

]
